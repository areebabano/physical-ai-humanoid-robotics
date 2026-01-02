import os
import time
import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# -------------------------------------
# CONFIG
# -------------------------------------
SITEMAP_URL = os.getenv(
    "SITEMAP_URL",
    "https://physical-ai-humanoid-robotics-khbj.vercel.app/sitemap.xml"
)
COLLECTION_NAME = os.getenv("INGESTION_COLLECTION_NAME", "physical-ai-humanoid-robotics-book1")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 20))  # number of chunks per batch
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 5))

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
cohere_client = cohere.Client(cohere_api_key)
EMBED_MODEL = os.getenv("EMBED_MODEL", "embed-english-v3.0")

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

qdrant = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

# -------------------------------------
# STEP 1 — Extract URLs from sitemap
# -------------------------------------
def get_all_urls(sitemap_url):
    """
    Fetch all URLs from the sitemap XML
    Handles both regular sitemaps and sitemap indexes
    """
    response = requests.get(sitemap_url)
    response.raise_for_status()
    xml_content = response.text
    root = ET.fromstring(xml_content)

    urls = []
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Check if this is a sitemap index (contains sitemap elements)
    sitemap_elements = root.findall("sm:sitemap", namespace)
    if sitemap_elements:
        print("Found sitemap index, processing nested sitemaps...")
        for sitemap_elem in sitemap_elements:
            loc = sitemap_elem.find("sm:loc", namespace)
            if loc is not None:
                nested_sitemap_url = loc.text
                print(f"Processing nested sitemap: {nested_sitemap_url}")
                nested_response = requests.get(nested_sitemap_url)
                nested_response.raise_for_status()
                nested_root = ET.fromstring(nested_response.text)

                for url_elem in nested_root.findall("sm:url", namespace):
                    loc_tag = url_elem.find("sm:loc", namespace)
                    if loc_tag is not None:
                        url = loc_tag.text
                        # Fix domain mismatch if needed
                        if "physical-ai-humanoid-robotics-book.com" in url:
                            url = url.replace("physical-ai-humanoid-robotics-book.com",
                                              "physical-ai-humanoid-robotics-khbj.vercel.app")
                        urls.append(url)
    else:
        # This is a regular sitemap with URL elements
        for url_elem in root.findall("sm:url", namespace):
            loc_tag = url_elem.find("sm:loc", namespace)
            if loc_tag is not None:
                url = loc_tag.text
                # Fix domain mismatch if needed
                if "physical-ai-humanoid-robotics-book.com" in url:
                    url = url.replace("physical-ai-humanoid-robotics-book.com",
                                      "physical-ai-humanoid-robotics-khbj.vercel.app")
                urls.append(url)

    print("\nFOUND URLS:")
    for u in urls:
        print(" -", u)

    return urls

# -------------------------------------
# STEP 2 — Download page + extract text
# -------------------------------------
def extract_text_from_url(url):
    """
    Extract text content from a URL with proper error handling
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        text = trafilatura.extract(response.text)
        if not text:
            print(f"[WARNING] No text extracted from: {url}")
            return None
        return text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch URL {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"[ERROR] Error processing URL {url}: {str(e)}")
        return None

# -------------------------------------
# STEP 3 — Chunk the text (fast)
# -------------------------------------
import re

def chunk_text(text, max_chars=1200):
    """
    Split text into chunks of reasonable size with proper sentence boundaries
    """
    if len(text) <= max_chars:
        return [text.strip()]

    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding this sentence would exceed the limit
        if len(current_chunk) + len(sentence) > max_chars:
            # If current chunk is not empty, save it
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # If the sentence itself is longer than max_chars, split it
            if len(sentence) > max_chars:
                # Split the long sentence into smaller parts
                for i in range(0, len(sentence), max_chars):
                    chunks.append(sentence[i:i+max_chars].strip())
                current_chunk = ""
            else:
                current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "

    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out any empty chunks
    chunks = [chunk for chunk in chunks if chunk.strip()]
    return chunks

# -------------------------------------
# STEP 4 — Batch embedding
# -------------------------------------

def embed_batch(chunks):
    """
    Generate embeddings with retry logic for Rate Limits (429)
    """
    max_retries = 3
    retry_delay = 20  # 20 seconds wait if rate limited

    for attempt in range(max_retries):
        try:
            response = cohere_client.embed(
                model=EMBED_MODEL,
                input_type="search_document",
                texts=chunks
            )
            # Har successful request ke baad 12 second wait karein (Free Tier limit)
            print("Embedding successful. Waiting 12s for rate limit safety...")
            time.sleep(12) 
            return response.embeddings
        except Exception as e:
            if "429" in str(e):
                print(f"[RATE LIMIT] Hit limit, waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
            else:
                print(f"[ERROR] Failed to generate embeddings: {str(e)}")
                return None
    return None
# def embed_batch(chunks):
#     """
#     Generate embeddings for a batch of text chunks using Cohere
#     """
#     try:
#         response = cohere_client.embed(
#             model=EMBED_MODEL,
#             input_type="search_document",  # Use search_document for documents to be retrieved
#             texts=chunks
#         )
#         return response.embeddings
#     except Exception as e:
#         print(f"[ERROR] Failed to generate embeddings: {str(e)}")
#         # Return None to indicate failure
#         return None

# -------------------------------------
# STEP 5 — Qdrant collection setup
# -------------------------------------
def create_collection():
    print("\nCreating Qdrant collection...")
    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,  # Cohere embed-english-v3.0 dimension
            distance=Distance.COSINE
        )
    )

# -------------------------------------
# STEP 6 — Save chunks to Qdrant in batch
# -------------------------------------
def save_chunks_to_qdrant(chunks, start_id, url):
    """
    Save text chunks to Qdrant with their embeddings
    """
    if not chunks:
        print(f"No chunks to save for URL: {url}")
        return 0

    embeddings = embed_batch(chunks)
    if embeddings is None:
        print(f"Failed to generate embeddings for URL: {url}")
        return 0

    # Create points for Qdrant
    points = []
    for i, (vec, ch) in enumerate(zip(embeddings, chunks)):
        point = PointStruct(
            id=start_id + i,
            vector=vec,
            payload={
                "url": url,
                "text": ch,
                "chunk_id": start_id + i
            }
        )
        points.append(point)

    # Split into batches for Qdrant upsert
    for i in range(0, len(points), BATCH_SIZE):
        batch = points[i:i+BATCH_SIZE]
        qdrant.upsert(collection_name=COLLECTION_NAME, points=batch)

    print(f"Saved {len(chunks)} chunks for {url}")
    return len(chunks)

# -------------------------------------
# STEP 7 — Main ingestion pipeline
# -------------------------------------
def process_url(url, start_id):
    """
    Process a single URL: extract text, chunk it, and save to Qdrant
    """
    print("\nProcessing:", url)
    try:
        text = extract_text_from_url(url)
        if not text:
            print(f"Skipping {url} - no text extracted")
            return 0

        chunks = chunk_text(text)
        if not chunks:
            print(f"No chunks created for {url}")
            return 0

        saved_count = save_chunks_to_qdrant(chunks, start_id, url)
        return saved_count
    except Exception as e:
        print(f"[ERROR] Failed to process URL {url}: {str(e)}")
        return 0

def ingest_book():
    """
    Main ingestion pipeline: simple one-by-one processing to avoid rate limits
    """
    print("Starting content ingestion process...")
    urls = get_all_urls(SITEMAP_URL)
    create_collection()

    if not urls:
        print("No URLs found in sitemap. Exiting.")
        return

    total_chunks = 0
    global_id = 1

    # Parallel (ThreadPool) ki jagah simple Loop use karein
    for url in urls:
        try:
            # Process one URL at a time
            chunk_count = process_url(url, global_id)
            total_chunks += chunk_count
            global_id += chunk_count
            
            # Har URL ke baad thoda extra rest
            time.sleep(2) 
        except Exception as e:
            print(f"[ERROR] Skipping URL {url} due to: {e}")

    print("\n[SUCCESS] Ingestion completed!")
    print("Total chunks stored:", total_chunks)
    print(f"Processed {len(urls)} URLs")
# def ingest_book():
#     """
#     Main ingestion pipeline: fetch URLs from sitemap, extract content, embed, and store in Qdrant
#     """
#     print("Starting content ingestion process...")
#     urls = get_all_urls(SITEMAP_URL)
#     create_collection()

#     if not urls:
#         print("No URLs found in sitemap. Exiting.")
#         return

#     global_id = 1
#     id_increments = []  # Track actual increments to calculate next ID correctly

#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         futures = []
#         for url in urls:
#             futures.append(executor.submit(process_url, url, global_id))
#             # We'll calculate the actual increment after each URL is processed
#             # For now, we'll just process them and then calculate proper IDs later
#             # Actually, let's keep track properly by waiting for each one to get its actual chunk count
#             pass

#         total_chunks = 0
#         for f in futures:
#             chunk_count = f.result()
#             total_chunks += chunk_count
#             # Each future processes one URL, so we need to update global_id accordingly
#             # Since we don't know the chunk count until processing is done,
#             # we'll use a safe increment approach

#     print("\n[SUCCESS] Ingestion completed!")
#     print("Total chunks stored:", total_chunks)
#     print(f"Processed {len(urls)} URLs")


def main():
    """
    Main entry point for the ingestion script
    """
    try:
        ingest_book()
    except KeyboardInterrupt:
        print("\nIngestion interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] Ingestion failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
