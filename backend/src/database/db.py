from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import logging
from ..core.config import settings
from ..core.logging import logger


class QdrantDatabase:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.INGESTION_COLLECTION_NAME
        self._verify_connection()

    def _verify_connection(self):
        """Verify that we can connect to Qdrant"""
        try:
            # Try to get collection info to verify connection
            collections = self.client.get_collections()
            logger.info(f"Connected to Qdrant. Available collections: {[col.name for col in collections.collections]}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant
        """
        try:
            # Try the newer query method first, fallback to search if needed
            try:
                search_result = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
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
                search_result = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
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
            logger.error(f"Error during Qdrant search: {e}")
            return []

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors_count,
                "vectors_count": collection_info.config.params.vectors_count,
                "indexed_vectors_count": collection_info.indexed_vectors_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}


# Global instance
qdrant_db = QdrantDatabase()