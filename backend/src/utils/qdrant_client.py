"""
Qdrant client setup for the Physical AI & Humanoid Robotics Textbook
This module handles the connection and configuration for Qdrant vector database
"""
import os
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging


class QdrantSetup:
    """
    Setup and configuration for Qdrant vector database connection
    """

    def __init__(self):
        # Get Qdrant configuration from environment variables
        self.qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")

        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Initialize the Qdrant client
        if self.qdrant_api_key:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                timeout=10
            )
        else:
            self.client = QdrantClient(
                url=self.qdrant_url,
                timeout=10
            )

    async def initialize_collection(self):
        """
        Initialize the collection for textbook content with proper vector configuration
        """
        try:
            # Check if collection already exists
            collections = await self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with vector configuration
                # Using 1536 dimensions for OpenAI's text-embedding-ada-002 embeddings
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Standard size for text-embedding-ada-002
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload indexes for faster filtering
                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="content_type",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="module_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                await self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chapter_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                self.logger.info(f"Successfully created Qdrant collection: {self.collection_name}")
            else:
                self.logger.info(f"Qdrant collection {self.collection_name} already exists")

        except Exception as e:
            self.logger.error(f"Error initializing Qdrant collection: {str(e)}")
            raise

    async def health_check(self) -> bool:
        """
        Check if Qdrant server is accessible
        """
        try:
            # Get collections to test connection
            await self.client.get_collections()
            return True
        except Exception as e:
            self.logger.error(f"Qdrant health check failed: {str(e)}")
            return False

    def get_client(self) -> QdrantClient:
        """
        Get the initialized Qdrant client
        """
        return self.client

    def get_collection_name(self) -> str:
        """
        Get the configured collection name
        """
        return self.collection_name


# Global instance
qdrant_setup = QdrantSetup()


async def get_qdrant_client() -> QdrantClient:
    """
    Dependency to get Qdrant client for FastAPI
    """
    return qdrant_setup.get_client()


async def get_collection_name() -> str:
    """
    Dependency to get collection name
    """
    return qdrant_setup.get_collection_name()