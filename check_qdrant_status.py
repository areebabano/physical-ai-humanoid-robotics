import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Qdrant
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("INGESTION_COLLECTION_NAME", "physical-ai-humanoid_robotics_book1")

if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

qdrant = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

print(f"Checking Qdrant collection: {collection_name}")

# List all collections
collections = qdrant.get_collections()
print(f"Available collections: {[coll.name for coll in collections.collections]}")

# Check if our collection exists
collection_exists = qdrant.collection_exists(collection_name)
print(f"Collection '{collection_name}' exists: {collection_exists}")

if collection_exists:
    # Get collection info
    collection_info = qdrant.get_collection(collection_name)
    print(f"Collection points count: {collection_info.points_count}")
    # Note: vectors_count might not be available in all versions, so we'll handle it gracefully
    try:
        print(f"Collection vectors count: {collection_info.vectors_count}")
    except AttributeError:
        print("Collection vectors count: N/A (attribute not available in this version)")

    # Try to get a few points to see if there's actual data
    try:
        points = qdrant.scroll(
            collection_name=collection_name,
            limit=3  # Get first 3 points to verify content
        )
        print(f"\nSample points retrieved: {len(points[0]) if points[0] else 0}")
        for i, point in enumerate(points[0][:2]):  # Show first 2 points
            print(f"Point {i+1}:")
            print(f"  ID: {point.id}")
            print(f"  URL: {point.payload.get('url', 'N/A')}")
            print(f"  Text snippet: {point.payload.get('text', '')[:100]}...")
            print(f"  Score: N/A")
            print()
    except Exception as e:
        print(f"Error retrieving sample points: {e}")
else:
    print(f"Collection '{collection_name}' does not exist in Qdrant.")