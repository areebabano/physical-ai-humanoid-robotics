import os
import cohere
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")

cohere_client = cohere.Client(cohere_api_key)

# Connect to Qdrant
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

qdrant = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding

def retrieve(query, collection_name=None, limit=5):
    """
    Retrieve relevant chunks from Qdrant based on the query
    Returns top 5 chunks with score, URL, and text
    """
    # Use the collection name from environment or default to the ingestion collection
    if collection_name is None:
        collection_name = os.getenv("INGESTION_COLLECTION_NAME", "physical-ai-humanoid_robotics_book")

    embedding = get_embedding(query)

    try:
        # Try the newer query method first, fallback to search if needed
        search_result = qdrant.query_points(
            collection_name=collection_name,
            query=embedding,
            limit=limit
        )
        results = []
        for point in search_result.points:
            result = {
                "text": point.payload["text"],
                "url": point.payload["url"],
                "score": getattr(point, 'score', 0),
                "chunk_id": point.payload.get("chunk_id", "unknown")
            }
            results.append(result)
        return results
    except AttributeError:
        # Fallback to the search method if query_points is not available
        search_result = qdrant.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=limit
        )
        results = []
        for point in search_result:
            result = {
                "text": point.payload["text"],
                "url": point.payload["url"],
                "score": point.score,
                "chunk_id": point.payload.get("chunk_id", "unknown")
            }
            results.append(result)
        return results
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []

def retrieve_with_context(query, limit=5):
    """
    Retrieve relevant chunks with additional context information
    """
    collection_name = os.getenv("INGESTION_COLLECTION_NAME", "physical-ai-humanoid_robotics_book")
    embedding = get_embedding(query)

    try:
        # Try the newer query method first, fallback to search if needed
        search_result = qdrant.query_points(
            collection_name=collection_name,
            query=embedding,
            limit=limit
        )
        results = []
        for point in search_result.points:
            result = {
                "text": point.payload["text"],
                "url": point.payload["url"],
                "chunk_id": point.payload.get("chunk_id", "unknown"),
                "score": getattr(point, 'score', 0),  # Use getattr to safely get score
            }
            results.append(result)
        return results
    except AttributeError:
        # Fallback to the search method if query_points is not available
        search_result = qdrant.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=limit
        )
        results = []
        for point in search_result:
            result = {
                "text": point.payload["text"],
                "url": point.payload["url"],
                "chunk_id": point.payload.get("chunk_id", "unknown"),
                "score": point.score
            }
            results.append(result)
        return results
    except Exception as e:
        print(f"Error during retrieval with context: {e}")
        return []

def main():
    """
    Main function to test the retrieval system
    """
    print("Testing retrieval from the ingested content...")
    print("Query: 'What is humanoid robotics?'")

    results = retrieve_with_context("What is humanoid robotics?")

    if results:
        print(f"\nFound {len(results)} relevant chunks:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['score']:.4f}")
            print(f"   URL: {result['url']}")
            print(f"   Chunk ID: {result['chunk_id']}")
            print(f"   Text: {result['text'][:300]}...")  # Show more text
    else:
        print("No results found. Make sure:")
        print("1. The content ingestion completed successfully")
        print("2. The Qdrant collection exists and has data")
        print("3. Your API keys are correct")
        print("4. The collection name matches what was used during ingestion")

    # Test another query
    print("\n" + "="*50)
    print("Testing another query: 'What is physical AI?'")
    results2 = retrieve_with_context("What is physical AI?")

    if results2:
        print(f"\nFound {len(results2)} relevant chunks:")
        for i, result in enumerate(results2, 1):
            print(f"\n{i}. Score: {result['score']:.4f}")
            print(f"   URL: {result['url']}")
            print(f"   Chunk ID: {result['chunk_id']}")
            print(f"   Text: {result['text'][:300]}...")
    else:
        print("No results found for second query.")


if __name__ == "__main__":
    main()