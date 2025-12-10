"""
Content indexer utility for the Physical AI & Humanoid Robotics Textbook
Handles indexing of textbook content for RAG chatbot functionality
"""
import asyncio
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import AsyncOpenAI
import os
import logging


class ContentIndexer:
    """
    Service for indexing textbook content into Qdrant vector database
    """

    def __init__(self):
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_api_key:
            self.qdrant_client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key
            )
        else:
            self.qdrant_client = QdrantClient(url=qdrant_url)

        # Initialize OpenAI client for embedding generation
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.openai_client = AsyncOpenAI(api_key=openai_api_key)

        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Define collection name
        self.collection_name = "textbook_content"

    async def initialize_collection(self):
        """
        Initialize the Qdrant collection for storing textbook content
        """
        try:
            # Check if collection already exists
            collections = await self.qdrant_client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create collection with vector configuration
                await self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Default size for text-embedding-ada-002
                        distance=models.Distance.COSINE
                    )
                )

                # Create payload index for content type
                await self.qdrant_client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="content_type",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                # Create payload index for module_id
                await self.qdrant_client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="module_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                self.logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                self.logger.info(f"Qdrant collection {self.collection_name} already exists")

        except Exception as e:
            self.logger.error(f"Error initializing Qdrant collection: {e}")
            raise

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        """
        try:
            response = await self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            raise

    async def index_content(self, content_id: str, content: str, content_type: str,
                           module_id: str, chapter_id: str = None, metadata: Dict[str, Any] = None):
        """
        Index a piece of content in Qdrant
        """
        try:
            # Generate embedding for the content
            embedding = await self.generate_embedding(content)

            # Prepare payload
            payload = {
                "content_type": content_type,
                "module_id": module_id,
                "content": content,
                "indexed_at": asyncio.get_event_loop().time()
            }

            if chapter_id:
                payload["chapter_id"] = chapter_id

            if metadata:
                payload.update(metadata)

            # Prepare points for upsert
            points = [
                models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload=payload
                )
            ]

            # Upsert the content into Qdrant
            await self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            self.logger.info(f"Indexed content {content_id} of type {content_type}")

        except Exception as e:
            self.logger.error(f"Error indexing content {content_id}: {e}")
            raise

    async def index_module(self, module_id: str, module_title: str, module_content: str,
                          chapters_data: List[Dict[str, Any]]):
        """
        Index an entire module with its chapters
        """
        try:
            # Index module overview
            await self.index_content(
                content_id=f"module_{module_id}",
                content=f"Module: {module_title}. {module_content}",
                content_type="module",
                module_id=module_id,
                metadata={"title": module_title}
            )

            # Index each chapter
            for chapter_data in chapters_data:
                chapter_id = chapter_data.get("id")
                chapter_title = chapter_data.get("title")
                chapter_content = chapter_data.get("content")
                learning_objectives = chapter_data.get("learning_objectives", [])

                # Combine chapter content with learning objectives
                full_content = f"Chapter: {chapter_title}. {chapter_content}"
                if learning_objectives:
                    full_content += f" Learning objectives: {'; '.join(learning_objectives)}"

                await self.index_content(
                    content_id=f"chapter_{chapter_id}",
                    content=full_content,
                    content_type="chapter",
                    module_id=module_id,
                    chapter_id=chapter_id,
                    metadata={"title": chapter_title}
                )

                # Index exercises if they exist
                exercises = chapter_data.get("exercises", [])
                for i, exercise in enumerate(exercises):
                    exercise_id = f"{chapter_id}_ex_{i}"
                    exercise_content = f"Exercise: {exercise.get('question', '')}"
                    if exercise.get('options'):
                        exercise_content += f" Options: {'; '.join(exercise['options'])}"

                    await self.index_content(
                        content_id=exercise_id,
                        content=exercise_content,
                        content_type="exercise",
                        module_id=module_id,
                        chapter_id=chapter_id,
                        metadata={"title": f"Exercise in {chapter_title}"}
                    )

            self.logger.info(f"Indexed module {module_id} with {len(chapters_data)} chapters")

        except Exception as e:
            self.logger.error(f"Error indexing module {module_id}: {e}")
            raise

    async def search_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for content in the index
        """
        try:
            # Generate embedding for the query
            query_embedding = await self.generate_embedding(query)

            # Search in Qdrant
            search_results = await self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "content_type": result.payload.get("content_type"),
                    "module_id": result.payload.get("module_id"),
                    "chapter_id": result.payload.get("chapter_id"),
                    "title": result.payload.get("title", ""),
                    "relevance_score": result.score
                })

            return results

        except Exception as e:
            self.logger.error(f"Error searching content: {e}")
            raise

    async def delete_content(self, content_id: str):
        """
        Delete a specific content from the index
        """
        try:
            await self.qdrant_client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[content_id]
                )
            )
            self.logger.info(f"Deleted content {content_id} from index")
        except Exception as e:
            self.logger.error(f"Error deleting content {content_id}: {e}")
            raise

    async def clear_collection(self):
        """
        Clear all content from the collection (use with caution!)
        """
        try:
            await self.qdrant_client.delete_collection(self.collection_name)
            await self.initialize_collection()
            self.logger.info(f"Cleared and reinitialized collection {self.collection_name}")
        except Exception as e:
            self.logger.error(f"Error clearing collection: {e}")
            raise


# Singleton instance
content_indexer = ContentIndexer()