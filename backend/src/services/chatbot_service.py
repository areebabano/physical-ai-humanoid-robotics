# # # # # # # # import cohere
# # # # # # # # from typing import List, Dict, Any
# # # # # # # # import logging
# # # # # # # # from ..core.config import settings
# # # # # # # # from ..core.logging import logger
# # # # # # # # from ..database.db import qdrant_db


# # # # # # # # class ChatbotService:
# # # # # # # #     def __init__(self):
# # # # # # # #         # Initialize Cohere client
# # # # # # # #         if not settings.COHERE_API_KEY:
# # # # # # # #             raise ValueError("COHERE_API_KEY environment variable is required")

# # # # # # # #         self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
# # # # # # # #         self.embed_model = settings.EMBED_MODEL
# # # # # # # #         self.generation_model = settings.GENERATION_MODEL
# # # # # # # #         self.max_tokens = settings.MAX_TOKENS
# # # # # # # #         self.temperature = settings.TEMPERATURE

# # # # # # # #     def get_embedding(self, text: str) -> List[float]:
# # # # # # # #         """Get embedding vector from Cohere Embed v3"""
# # # # # # # #         try:
# # # # # # # #             response = self.cohere_client.embed(
# # # # # # # #                 model=self.embed_model,
# # # # # # # #                 input_type="search_query",  # Use search_query for queries
# # # # # # # #                 texts=[text],
# # # # # # # #             )
# # # # # # # #             return response.embeddings[0]  # Return the first embedding
# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"Error generating embedding: {e}")
# # # # # # # #             raise

# # # # # # # #     def retrieve(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
# # # # # # # #         """
# # # # # # # #         Retrieve relevant content from Qdrant based on the query
# # # # # # # #         Returns top chunks with score, URL, and text
# # # # # # # #         """
# # # # # # # #         if limit is None:
# # # # # # # #             limit = settings.RETRIEVAL_LIMIT

# # # # # # # #         try:
# # # # # # # #             embedding = self.get_embedding(query)
# # # # # # # #             results = qdrant_db.search(embedding, limit=limit)
# # # # # # # #             return results
# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"Error during retrieval: {e}")
# # # # # # # #             return []

# # # # # # # #     def generate_response(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
# # # # # # # #         """
# # # # # # # #         Generate a response based on the query and retrieved chunks
# # # # # # # #         Uses Cohere to generate the response from the retrieved content
# # # # # # # #         """
# # # # # # # #         if not retrieved_chunks:
# # # # # # # #             return "I don't know. The information was not found in the textbook content."

# # # # # # # #         # Combine the top retrieved chunks to form context
# # # # # # # #         context_parts = []
# # # # # # # #         for chunk in retrieved_chunks:
# # # # # # # #             context_parts.append(f"Source: {chunk['url']}\nContent: {chunk['text'][:500]}...")  # Limit content length

# # # # # # # #         context = "\n\n".join(context_parts)

# # # # # # # #         # Prepare the prompt for Cohere
# # # # # # # #         prompt = f"""
# # # # # # # #         You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # # # #         Answer the user's question based ONLY on the provided context from the textbook.
# # # # # # # #         If the answer is not in the provided context, say "I don't know. The information was not found in the textbook content."

# # # # # # # #         Question: {query}

# # # # # # # #         Context from textbook:
# # # # # # # #         {context}

# # # # # # # #         Answer:
# # # # # # # #         """

# # # # # # # #         try:
# # # # # # # #             response = self.cohere_client.generate(
# # # # # # # #                 model=self.generation_model,
# # # # # # # #                 prompt=prompt,
# # # # # # # #                 max_tokens=self.max_tokens,
# # # # # # # #                 temperature=self.temperature,
# # # # # # # #             )

# # # # # # # #             return response.generations[0].text.strip()
# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"Error generating response: {e}")
# # # # # # # #             # Fallback: return the raw content from chunks
# # # # # # # #             fallback_response = "Based on the textbook content:\n\n"
# # # # # # # #             for i, chunk in enumerate(retrieved_chunks[:3]):  # Use top 3 chunks
# # # # # # # #                 fallback_response += f"{i+1}. From {chunk['url']}:\n{chunk['text'][:300]}...\n\n"
# # # # # # # #             return fallback_response

# # # # # # # #     def process_chat(self, query: str, selected_text: str = None) -> Dict[str, Any]:
# # # # # # # #         """
# # # # # # # #         Process a chat query using RAG
# # # # # # # #         """
# # # # # # # #         try:
# # # # # # # #             logger.info(f"Processing query: {query}")

# # # # # # # #             # If selected text is provided, prepend it to the query for more context
# # # # # # # #             if selected_text:
# # # # # # # #                 full_query = f"{selected_text}\n\n{query}"
# # # # # # # #             else:
# # # # # # # #                 full_query = query

# # # # # # # #             # Retrieve relevant content from Qdrant
# # # # # # # #             retrieved_chunks = self.retrieve(full_query)

# # # # # # # #             # Generate response based on retrieved content
# # # # # # # #             response_text = self.generate_response(full_query, retrieved_chunks)

# # # # # # # #             # Extract unique source URLs
# # # # # # # #             sources = list(set([chunk['url'] for chunk in retrieved_chunks if chunk['url']]))

# # # # # # # #             # Limit to top 5 sources
# # # # # # # #             sources = sources[:5]

# # # # # # # #             result = {
# # # # # # # #                 "response": response_text,
# # # # # # # #                 "conversation_id": "default_conversation",
# # # # # # # #                 "sources": sources,
# # # # # # # #                 "retrieved_chunks": retrieved_chunks  # Include for debugging if needed
# # # # # # # #             }

# # # # # # # #             logger.info(f"Response generated successfully, sources: {len(sources)}")
# # # # # # # #             return result

# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"Error in chat processing: {e}")
# # # # # # # #             raise


# # # # # # # # # Global instance
# # # # # # # # chatbot_service = ChatbotService()

# # # # # # # # backend/src/services/chatbot_service.py

# # # # # # # import os
# # # # # # # import logging
# # # # # # # from typing import List, Dict, Any
# # # # # # # from dotenv import load_dotenv
# # # # # # # import cohere
# # # # # # # from ..database.db import qdrant_db
# # # # # # # from ..core.config import settings
# # # # # # # from ..core.logging import logger

# # # # # # # # Load environment variables
# # # # # # # load_dotenv()


# # # # # # # class ChatbotService:
# # # # # # #     """
# # # # # # #     Chatbot Service: Handles RAG pipeline using Cohere embeddings
# # # # # # #     and Qdrant vector DB retrieval.
# # # # # # #     """

# # # # # # #     def __init__(self):
# # # # # # #         # Initialize Cohere client
# # # # # # #         cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # # # #         if not cohere_api_key:
# # # # # # #             raise ValueError("COHERE_API_KEY environment variable is required")
# # # # # # #         self.cohere_client = cohere.Client(cohere_api_key)

# # # # # # #         # Model configs
# # # # # # #         self.embed_model = settings.EMBED_MODEL or "embed-english-v3.0"
# # # # # # #         self.generation_model = settings.GENERATION_MODEL or "command-r-plus"
# # # # # # #         self.max_tokens = settings.MAX_TOKENS or 500
# # # # # # #         self.temperature = settings.TEMPERATURE or 0.3
# # # # # # #         self.retrieval_limit = settings.RETRIEVAL_LIMIT or 5

# # # # # # #     def get_embedding(self, text: str) -> List[float]:
# # # # # # #         """Get embedding vector from Cohere Embed API"""
# # # # # # #         try:
# # # # # # #             response = self.cohere_client.embed(
# # # # # # #                 model=self.embed_model,
# # # # # # #                 input_type="search_query",
# # # # # # #                 texts=[text]
# # # # # # #             )
# # # # # # #             return response.embeddings[0]
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Error generating embedding: {e}")
# # # # # # #             raise

# # # # # # #     def retrieve(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
# # # # # # #         """Retrieve relevant content from Qdrant based on query embeddings"""
# # # # # # #         if limit is None:
# # # # # # #             limit = self.retrieval_limit
# # # # # # #         try:
# # # # # # #             embedding = self.get_embedding(query)
# # # # # # #             results = qdrant_db.search(embedding, limit=limit)
# # # # # # #             return results
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Error during retrieval: {e}")
# # # # # # #             return []

# # # # # # #     def generate_response(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
# # # # # # #         """Generate response using Cohere API and retrieved Qdrant content"""
# # # # # # #         if not retrieved_chunks:
# # # # # # #             return "I don't know. The information was not found in the textbook content."

# # # # # # #         context = "\n\n".join([
# # # # # # #             f"Source: {chunk['url']}\nContent: {chunk['text'][:500]}..."
# # # # # # #             for chunk in retrieved_chunks
# # # # # # #         ])

# # # # # # #         prompt = f"""
# # # # # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # # # Answer the user's question based ONLY on the provided context from the textbook.
# # # # # # # If the answer is not in the provided context, say "I don't know. The information was not found in the textbook content."

# # # # # # # Question: {query}

# # # # # # # Context from textbook:
# # # # # # # {context}

# # # # # # # Answer:
# # # # # # # """
# # # # # # #         try:
# # # # # # #             response = self.cohere_client.generate(
# # # # # # #                 model=self.generation_model,
# # # # # # #                 prompt=prompt,
# # # # # # #                 max_tokens=self.max_tokens,
# # # # # # #                 temperature=self.temperature
# # # # # # #             )
# # # # # # #             return response.generations[0].text.strip()
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Error generating response: {e}")
# # # # # # #             # fallback: show top chunks
# # # # # # #             fallback = "Based on the textbook content:\n\n"
# # # # # # #             for i, chunk in enumerate(retrieved_chunks[:3]):
# # # # # # #                 fallback += f"{i+1}. From {chunk['url']}:\n{chunk['text'][:300]}...\n\n"
# # # # # # #             return fallback

# # # # # # #     def process_chat(self, query: str, selected_text: str = None) -> Dict[str, Any]:
# # # # # # #         """Full RAG pipeline: retrieve + generate response"""
# # # # # # #         try:
# # # # # # #             full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # # # # #             retrieved_chunks = self.retrieve(full_query)
# # # # # # #             response_text = self.generate_response(full_query, retrieved_chunks)
# # # # # # #             sources = list({chunk['url'] for chunk in retrieved_chunks if chunk['url']})[:5]

# # # # # # #             return {
# # # # # # #                 "response": response_text,
# # # # # # #                 "conversation_id": "default_conversation",
# # # # # # #                 "sources": sources,
# # # # # # #                 "retrieved_chunks": retrieved_chunks
# # # # # # #             }
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Error in chat processing: {e}")
# # # # # # #             raise


# # # # # # # Global instance to use in FastAPI
# # # # # # # chatbot_service = ChatbotService()

# # # # # # # # backend/src/services/chatbot_service.py

# # # # # # # import os
# # # # # # # from typing import List, Dict, Any
# # # # # # # from dotenv import load_dotenv
# # # # # # # import cohere
# # # # # # # from qdrant_client import QdrantClient
# # # # # # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # # # # # from ..core.config import settings
# # # # # # # from ..core.logging import logger

# # # # # # # # Load environment variables
# # # # # # # load_dotenv()
# # # # # # # enable_verbose_stdout_logging()
# # # # # # # set_tracing_disabled(disabled=True)

# # # # # # # # -----------------------------
# # # # # # # # Initialize Cohere (for embeddings)
# # # # # # # # -----------------------------
# # # # # # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # # # # if not cohere_api_key:
# # # # # # #     raise ValueError("COHERE_API_KEY is required")
# # # # # # # cohere_client = cohere.Client(cohere_api_key)

# # # # # # # # Initialize Qdrant
# # # # # # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # # # # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # # # # # if not qdrant_url:
# # # # # # #     raise ValueError("QDRANT_URL is required")
# # # # # # # qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)


# # # # # # # # -----------------------------
# # # # # # # # Gemini LLM Setup
# # # # # # # # -----------------------------
# # # # # # # gemini_api_key = os.getenv("GEMINI_API_KEY")
# # # # # # # if not gemini_api_key:
# # # # # # #     raise ValueError("GEMINI_API_KEY is required")

# # # # # # # provider = AsyncOpenAI(
# # # # # # #     api_key=gemini_api_key,
# # # # # # #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# # # # # # # )

# # # # # # # model = OpenAIChatCompletionsModel(
# # # # # # #     model="gemini-2.0-flash",
# # # # # # #     openai_client=provider
# # # # # # # )


# # # # # # # # -----------------------------
# # # # # # # # Embedding + Retrieval Tools
# # # # # # # # -----------------------------
# # # # # # # def get_embedding(text: str) -> List[float]:
# # # # # # #     """Get embedding vector from Cohere Embed API"""
# # # # # # #     response = cohere_client.embed(
# # # # # # #         model="embed-english-v3.0",
# # # # # # #         input_type="search_query",
# # # # # # #         texts=[text]
# # # # # # #     )
# # # # # # #     return response.embeddings[0]


# # # # # # # def get_retrieved_chunks(query: str):
# # # # # # #     embedding = get_embedding(query)
# # # # # # #     search_result = qdrant.search(
# # # # # # #         collection_name="physical-ai-humanoid_robotics",
# # # # # # #         query_vector=embedding,
# # # # # # #         limit=5,
# # # # # # #         with_payload=True
# # # # # # #     )
# # # # # # #     # Convert to list of dicts
# # # # # # #     chunks = []
# # # # # # #     for point in search_result:
# # # # # # #         chunks.append({
# # # # # # #             "text": point.payload.get("text", ""),
# # # # # # #             "url": point.payload.get("url", "")
# # # # # # #         })
# # # # # # #     return chunks
# # # # # # # # @function_tool
# # # # # # # # def retrieve(query: str) -> List[str]:
# # # # # # # #     """Retrieve top relevant chunks from Qdrant"""
# # # # # # # #     embedding = get_embedding(query)
# # # # # # # #     result = qdrant.search(
# # # # # # # #         collection_name="humanoid_ai_book",  # replace with your collection
# # # # # # # #         query_vector=embedding,
# # # # # # # #         limit=5
# # # # # # # #     )
# # # # # # # #     return [point.payload["text"] for point in result]


# # # # # # # # -----------------------------
# # # # # # # # RAG Agent
# # # # # # # # -----------------------------
# # # # # # # agent = Agent(
# # # # # # #     name="Physical AI Tutor",
# # # # # # #     instructions="""
# # # # # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # # # To answer the user question, first call the tool `retrieve` with the user query.
# # # # # # # Use ONLY the returned content from `retrieve` to answer.
# # # # # # # If the answer is not in the retrieved content, say "I don't know".
# # # # # # # """,
# # # # # # #     model=model,
# # # # # # #     tools=[get_retrieved_chunks]
# # # # # # # )


# # # # # # # # -----------------------------
# # # # # # # # Service Class
# # # # # # # # -----------------------------
# # # # # # # class ChatbotService:
# # # # # # #     """Full RAG pipeline using Cohere embeddings + Qdrant retrieval + Gemini for LLM"""

# # # # # # #     async def process_chat(self, query: str, selected_text: str = None) -> Dict[str, Any]:
# # # # # # #         try:
# # # # # # #             full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # # # # #             logger.info(f"Processing query: {full_query}")

# # # # # # #             # Run agent asynchronously
# # # # # # #             # retrieved_chunks = retrieve(full_query)
# # # # # # #             retrieved_chunks = get_retrieved_chunks(full_query)
# # # # # # #             result = await Runner.run(agent, input=full_query)
# # # # # # #             response_text = result.final_output

# # # # # # #             # Tool outputs se sources extract karo
# # # # # # #             sources = []
# # # # # # #             for tool_output in result.tool_outputs or []:
# # # # # # #                 if isinstance(tool_output, list):
# # # # # # #                     sources.extend(tool_output)

# # # # # # #             return {
# # # # # # #                 "response": response_text,
# # # # # # #                 "conversation_id": "default_conversation",
# # # # # # #                 "sources": [chunk['url'] for chunk in retrieved_chunks[:5]]
# # # # # # #             }

# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Error in chat processing: {e}")
# # # # # # #             return {"response": "An error occurred while processing your query."}


# # # # # # # # -----------------------------
# # # # # # # # Global instance to use in FastAPI
# # # # # # # # -----------------------------
# # # # # # # chatbot_service = ChatbotService()
# # # # # # # backend/src/services/chatbot_service.py

# # # # # # # import os
# # # # # # # from typing import List, Dict, Any
# # # # # # # from dotenv import load_dotenv
# # # # # # # import cohere
# # # # # # # from qdrant_client import QdrantClient
# # # # # # # from qdrant_client.http.models import Filter, PointStruct
# # # # # # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # # # # # from ..core.config import settings
# # # # # # # from ..core.logging import logger

# # # # # # # # Load environment variables
# # # # # # # load_dotenv()
# # # # # # # enable_verbose_stdout_logging()
# # # # # # # set_tracing_disabled(disabled=True)

# # # # # # # # -----------------------------
# # # # # # # # Initialize Cohere (for embeddings)
# # # # # # # # -----------------------------
# # # # # # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # # # # if not cohere_api_key:
# # # # # # #     raise ValueError("COHERE_API_KEY is required")
# # # # # # # cohere_client = cohere.Client(cohere_api_key)

# # # # # # # # Initialize Qdrant
# # # # # # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # # # # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # # # # # if not qdrant_url:
# # # # # # #     raise ValueError("QDRANT_URL is required")
# # # # # # # qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)


# # # # # # # # -----------------------------
# # # # # # # # Gemini LLM Setup
# # # # # # # # -----------------------------
# # # # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # # # if not groq_api_key:
# # # # # # #     raise ValueError("GROQ_API_KEY is required")

# # # # # # # provider = AsyncOpenAI(
# # # # # # #     api_key=groq_api_key,
# # # # # # #     base_url="https://api.groq.com/openai/v1"
# # # # # # # )

# # # # # # # model = OpenAIChatCompletionsModel(
# # # # # # #     model="llama-3.3-70b-versatile",
# # # # # # #     openai_client=provider
# # # # # # # )


# # # # # # # # -----------------------------
# # # # # # # # Embedding + Retrieval Tools
# # # # # # # # -----------------------------
# # # # # # # def get_embedding(text: str) -> List[float]:
# # # # # # #     """Get embedding vector from Cohere Embed API"""
# # # # # # #     response = cohere_client.embed(
# # # # # # #         model=settings.EMBED_MODEL or "embed-english-v3.0",
# # # # # # #         input_type="search_query",
# # # # # # #         texts=[text]
# # # # # # #     )
# # # # # # #     return response.embeddings[0]


# # # # # # # @function_tool
# # # # # # # def retrieve(query):
# # # # # # #     embedding = get_embedding(query)
# # # # # # #     result = qdrant.query_points(
# # # # # # #         collection_name="physical-ai-humanoid_robotics_book",
# # # # # # #         query=embedding,
# # # # # # #         limit=5
# # # # # # #     )
# # # # # # #     return [point.payload["text"] for point in result.points]


# # # # # # # # -----------------------------
# # # # # # # # RAG Agent
# # # # # # # # -----------------------------
# # # # # # # agent = Agent(
# # # # # # #     name="Physical AI Tutor",
# # # # # # #     instructions="""
# # # # # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # # # To answer the user question, first call the tool `retrieve` with the user query.
# # # # # # # Use ONLY the returned content from `retrieve` to answer.
# # # # # # # If the answer is not in the retrieved content, say "I don't know".
# # # # # # # """,
# # # # # # #     model=model,
# # # # # # #     tools=[retrieve],
    
# # # # # # # )


# # # # # # # # -----------------------------
# # # # # # # # Service Class
# # # # # # # # -----------------------------
# # # # # # # class ChatbotService:
# # # # # # #     """Full RAG pipeline using Cohere embeddings + Qdrant retrieval + Gemini LLM"""

# # # # # # #     async def process_chat(self, query: str, selected_text: str = None, conversation_id: str | None = None) -> Dict[str, Any]:
# # # # # # #         try:
# # # # # # #             conversation_id = conversation_id or "default_conversation"
# # # # # # #             full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # # # # #             logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# # # # # # #             # Run agent asynchronously
# # # # # # #             result = await Runner.run(agent, input=full_query)
# # # # # # #             response_text = result.final_output

# # # # # # #             # Extract sources from tool outputs
# # # # # # #             sources = []
# # # # # # #             if hasattr(result, "tools") and result.tools:
# # # # # # #                 for tool in result.tools:
# # # # # # #                     if tool.output and isinstance(tool.output, list):
# # # # # # #                         for item in tool.output:
# # # # # # #                             if isinstance(item, dict) and "url" in item:
# # # # # # #                                 sources.append(item["url"])

# # # # # # #             return {
# # # # # # #                 "response": response_text,
# # # # # # #                 "conversation_id": conversation_id,
# # # # # # #                 "sources": sources[:5]  # limit to top 5 sources
# # # # # # #             }

# # # # # # #         except Exception as e:
# # # # # # #             logger.exception("Chat processing failed")
# # # # # # #             return {
# # # # # # #                 "response": "An internal error occurred.",
# # # # # # #                 "conversation_id": conversation_id or "default_conversation",
# # # # # # #                 "sources": []
# # # # # # #             }


# # # # # # # # -----------------------------
# # # # # # # # Global instance to use in FastAPI
# # # # # # # # -----------------------------
# # # # # # # chatbot_service = ChatbotService()
# # # # # # import os
# # # # # # from typing import List, Dict, Any
# # # # # # from dotenv import load_dotenv
# # # # # # import cohere
# # # # # # from qdrant_client import QdrantClient
# # # # # # from qdrant_client.models import SearchRequest
# # # # # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # # # # from ..core.config import settings
# # # # # # from ..core.logging import logger

# # # # # # load_dotenv()
# # # # # # enable_verbose_stdout_logging()
# # # # # # set_tracing_disabled(disabled=True)

# # # # # # # -----------------------------
# # # # # # # Cohere Embeddings
# # # # # # # -----------------------------
# # # # # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # # # if not cohere_api_key:
# # # # # #     raise ValueError("COHERE_API_KEY is required")
# # # # # # cohere_client = cohere.Client(cohere_api_key)

# # # # # # # -----------------------------
# # # # # # # Qdrant Setup
# # # # # # # -----------------------------
# # # # # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # # # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # # # # if not qdrant_url:
# # # # # #     raise ValueError("QDRANT_URL is required")
# # # # # # qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# # # # # # # -----------------------------
# # # # # # # Gemini LLM Setup
# # # # # # # -----------------------------
# # # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # # if not groq_api_key:
# # # # # #     raise ValueError("GROQ_API_KEY is required")

# # # # # # provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# # # # # # model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=provider)

# # # # # # # -----------------------------
# # # # # # # Embedding + Retrieval Tools
# # # # # # # -----------------------------
# # # # # # async def get_embedding(text: str) -> List[float]:
# # # # # #     """Async embedding using Cohere"""
# # # # # #     response = cohere_client.embed(
# # # # # #         model=settings.EMBED_MODEL or "embed-english-v3.0",
# # # # # #         input_type="search_query",
# # # # # #         texts=[text]
# # # # # #     )
# # # # # #     return response.embeddings[0]

# # # # # # @function_tool
# # # # # # async def retrieve(query: str) -> List[str]:
# # # # # #     embedding = await get_embedding(query)
# # # # # #     result = qdrant.search(
# # # # # #         collection_name="physical-ai-humanoid_robotics_book",
# # # # # #         query_vector=embedding,
# # # # # #         limit=5
# # # # # #     )
# # # # # #     return [point.payload.get("text", "") for point in result]

# # # # # # # -----------------------------
# # # # # # # Agent
# # # # # # # -----------------------------
# # # # # # agent = Agent(
# # # # # #     name="Physical AI Tutor",
# # # # # #     instructions="""
# # # # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # # To answer the user question, first call the tool `retrieve` with the user query.
# # # # # # Use ONLY the returned content from `retrieve` to answer.
# # # # # # If the answer is not in the retrieved content, say "I don't know".
# # # # # # """,
# # # # # #     model=model,
# # # # # #     tools=[retrieve],
# # # # # # )

# # # # # # # -----------------------------
# # # # # # # Service Class
# # # # # # # -----------------------------
# # # # # # class ChatbotService:
# # # # # #     """Full async RAG pipeline"""

# # # # # #     async def process_chat(self, query: str, selected_text: str = None, conversation_id: str | None = None) -> Dict[str, Any]:
# # # # # #         conversation_id = conversation_id or "default_conversation"
# # # # # #         full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # # # #         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# # # # # #         try:
# # # # # #             result = await Runner.run(agent, input=full_query)
# # # # # #             response_text = getattr(result, "final_output", "I don't know")

# # # # # #             # Extract sources from tool calls
# # # # # #             sources = []
# # # # # #             for call in getattr(result, "tool_calls", []):
# # # # # #                 output = getattr(call, "output", None)
# # # # # #                 if output and isinstance(output, list):
# # # # # #                     for item in output:
# # # # # #                         if isinstance(item, dict) and "url" in item:
# # # # # #                             sources.append(item["url"])

# # # # # #             return {"response": response_text, "conversation_id": conversation_id, "sources": sources[:5]}

# # # # # #         except Exception:
# # # # # #             logger.exception("Chat processing failed")
# # # # # #             return {"response": "An internal error occurred.", "conversation_id": conversation_id, "sources": []}

# # # # # # # -----------------------------
# # # # # # # Global instance
# # # # # # # -----------------------------
# # # # # # chatbot_service = ChatbotService()
# # # # # import os
# # # # # from typing import List, Dict, Any
# # # # # from dotenv import load_dotenv
# # # # # import cohere
# # # # # from qdrant_client import QdrantClient
# # # # # from qdrant_client.models import Filter, PointStruct
# # # # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # # # from ..core.config import settings
# # # # # from ..core.logging import logger

# # # # # load_dotenv()
# # # # # enable_verbose_stdout_logging()
# # # # # set_tracing_disabled(disabled=True)

# # # # # # -----------------------------
# # # # # # Cohere Embeddings
# # # # # # -----------------------------
# # # # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # # if not cohere_api_key:
# # # # #     raise ValueError("COHERE_API_KEY is required")
# # # # # cohere_client = cohere.Client(cohere_api_key)

# # # # # # -----------------------------
# # # # # # Qdrant Setup
# # # # # # -----------------------------
# # # # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # # # if not qdrant_url:
# # # # #     raise ValueError("QDRANT_URL is required")

# # # # # # Initialize Qdrant client
# # # # # try:
# # # # #     qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
# # # # #     # Test connection
# # # # #     collections = qdrant.get_collections()
# # # # #     logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
# # # # # except Exception as e:
# # # # #     logger.error(f"Failed to connect to Qdrant: {e}")
# # # # #     raise

# # # # # # -----------------------------
# # # # # # Groq LLM Setup
# # # # # # -----------------------------
# # # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # # if not groq_api_key:
# # # # #     raise ValueError("GROQ_API_KEY is required")

# # # # # provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# # # # # model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=provider)

# # # # # # -----------------------------
# # # # # # Embedding + Retrieval Tools
# # # # # # -----------------------------
# # # # # async def get_embedding(text: str) -> List[float]:
# # # # #     """Generate embedding using Cohere"""
# # # # #     try:
# # # # #         response = cohere_client.embed(
# # # # #             model=settings.EMBED_MODEL or "embed-english-v3.0",
# # # # #             input_type="search_query",
# # # # #             texts=[text]
# # # # #         )
# # # # #         return response.embeddings[0]
# # # # #     except Exception as e:
# # # # #         logger.error(f"Embedding generation failed: {e}")
# # # # #         raise

# # # # # @function_tool
# # # # # async def retrieve(query: str) -> List[str]:
# # # # #     """Retrieve relevant documents from Qdrant vector database"""
# # # # #     try:
# # # # #         # Generate embedding for the query
# # # # #         embedding = await get_embedding(query)
# # # # #         logger.info(f"Generated embedding for query: {query}")
        
# # # # #         # Search in Qdrant (v1.16.2 syntax)
# # # # #         search_result = qdrant.search(
# # # # #             collection_name="physical-ai-humanoid_robotics_book",
# # # # #             query_vector=embedding,
# # # # #             limit=5
# # # # #         )
        
# # # # #         logger.info(f"Retrieved {len(search_result)} results from Qdrant")
        
# # # # #         # Extract text from payloads
# # # # #         texts = []
# # # # #         for point in search_result:
# # # # #             if point.payload and "text" in point.payload:
# # # # #                 texts.append(point.payload["text"])
        
# # # # #         return texts if texts else ["No relevant information found."]
        
# # # # #     except Exception as e:
# # # # #         logger.error(f"Retrieval failed: {e}")
# # # # #         return [f"Error during retrieval: {str(e)}"]

# # # # # # -----------------------------
# # # # # # Agent
# # # # # # -----------------------------
# # # # # agent = Agent(
# # # # #     name="Physical AI Tutor",
# # # # #     instructions="""
# # # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # # To answer the user question, first call the tool `retrieve` with the user query.
# # # # # Use ONLY the returned content from `retrieve` to answer.
# # # # # If the answer is not in the retrieved content, say "I don't know".
# # # # # Be clear, concise, and educational in your responses.
# # # # # """,
# # # # #     model=model,
# # # # #     tools=[retrieve],
# # # # # )

# # # # # # -----------------------------
# # # # # # Service Class
# # # # # # -----------------------------
# # # # # class ChatbotService:
# # # # #     """Full async RAG pipeline for Physical AI chatbot"""

# # # # #     async def process_chat(
# # # # #         self, 
# # # # #         query: str, 
# # # # #         selected_text: str = None, 
# # # # #         conversation_id: str | None = None
# # # # #     ) -> Dict[str, Any]:
# # # # #         """
# # # # #         Process a chat query using RAG pipeline
        
# # # # #         Args:
# # # # #             query: User's question
# # # # #             selected_text: Optional context from selected text
# # # # #             conversation_id: Optional conversation identifier
            
# # # # #         Returns:
# # # # #             Dict containing response, conversation_id, and sources
# # # # #         """
# # # # #         conversation_id = conversation_id or "default_conversation"
# # # # #         full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # # #         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# # # # #         try:
# # # # #             # Run the agent
# # # # #             result = await Runner.run(agent, input=full_query)
            
# # # # #             # Extract the final output
# # # # #             response_text = getattr(result, "final_output", "I don't know")
            
# # # # #             # Extract sources from tool calls if available
# # # # #             sources = []
# # # # #             tool_calls = getattr(result, "tool_calls", [])
# # # # #             for call in tool_calls:
# # # # #                 output = getattr(call, "output", None)
# # # # #                 if output and isinstance(output, list):
# # # # #                     for item in output:
# # # # #                         if isinstance(item, dict) and "url" in item:
# # # # #                             sources.append(item["url"])
            
# # # # #             logger.info(f"Conversation [{conversation_id}] - Response generated successfully")
            
# # # # #             return {
# # # # #                 "response": response_text,
# # # # #                 "conversation_id": conversation_id,
# # # # #                 "sources": sources[:5]
# # # # #             }

# # # # #         except Exception as e:
# # # # #             logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
# # # # #             return {
# # # # #                 "response": "An internal error occurred. Please try again.",
# # # # #                 "conversation_id": conversation_id,
# # # # #                 "sources": []
# # # # #             }

# # # # # # -----------------------------
# # # # # # Global instance
# # # # # # -----------------------------
# # # # # chatbot_service = ChatbotService()

# # # # import os
# # # # from typing import List, Dict, Any
# # # # from dotenv import load_dotenv
# # # # import cohere
# # # # from qdrant_client import QdrantClient
# # # # from qdrant_client.models import Filter, PointStruct
# # # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # # from ..core.config import settings
# # # # from ..core.logging import logger

# # # # load_dotenv()
# # # # enable_verbose_stdout_logging()
# # # # set_tracing_disabled(disabled=True)

# # # # # -----------------------------
# # # # # Cohere Embeddings
# # # # # -----------------------------
# # # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # # if not cohere_api_key:
# # # #     raise ValueError("COHERE_API_KEY is required")
# # # # cohere_client = cohere.Client(cohere_api_key)

# # # # # -----------------------------
# # # # # Qdrant Setup
# # # # # -----------------------------
# # # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # # if not qdrant_url:
# # # #     raise ValueError("QDRANT_URL is required")

# # # # # Initialize Qdrant client
# # # # try:
# # # #     qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
# # # #     # Test connection
# # # #     collections = qdrant.get_collections()
# # # #     logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
# # # # except Exception as e:
# # # #     logger.error(f"Failed to connect to Qdrant: {e}")
# # # #     raise

# # # # # -----------------------------
# # # # # Groq LLM Setup
# # # # # -----------------------------
# # # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # # if not groq_api_key:
# # # #     raise ValueError("GROQ_API_KEY is required")

# # # # provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# # # # # llama-3.1-70b-versatile has the best tool calling support on Groq
# # # # # Alternative options: "llama3-groq-70b-8192-tool-use-preview" or "mixtral-8x7b-32768"
# # # # model = OpenAIChatCompletionsModel(
# # # #     model="llama-3.1-70b-versatile",
# # # #     openai_client=provider
# # # # )

# # # # # -----------------------------
# # # # # Embedding + Retrieval Tools
# # # # # -----------------------------
# # # # async def get_embedding(text: str) -> List[float]:
# # # #     """Generate embedding using Cohere"""
# # # #     try:
# # # #         response = cohere_client.embed(
# # # #             model=settings.EMBED_MODEL or "embed-english-v3.0",
# # # #             input_type="search_query",
# # # #             texts=[text]
# # # #         )
# # # #         return response.embeddings[0]
# # # #     except Exception as e:
# # # #         logger.error(f"Embedding generation failed: {e}")
# # # #         raise

# # # # @function_tool
# # # # async def retrieve(query: str) -> str:
# # # #     """Retrieve relevant documents from Qdrant vector database
    
# # # #     Args:
# # # #         query: The search query string
        
# # # #     Returns:
# # # #         A string containing the retrieved information
# # # #     """
# # # #     try:
# # # #         # Generate embedding for the query
# # # #         embedding = await get_embedding(query)
# # # #         logger.info(f"Generated embedding for query: {query}")
        
# # # #         # Search in Qdrant (v1.16.2 syntax)
# # # #         search_result = qdrant.search(
# # # #             collection_name="physical-ai-humanoid_robotics_book",
# # # #             query_vector=embedding,
# # # #             limit=5
# # # #         )
        
# # # #         logger.info(f"Retrieved {len(search_result)} results from Qdrant")
        
# # # #         # Extract text from payloads and combine
# # # #         texts = []
# # # #         for point in search_result:
# # # #             if point.payload and "text" in point.payload:
# # # #                 texts.append(point.payload["text"])
        
# # # #         if texts:
# # # #             # Return combined text with separators
# # # #             return "\n\n---\n\n".join(texts)
# # # #         else:
# # # #             return "No relevant information found in the knowledge base."
        
# # # #     except Exception as e:
# # # #         logger.error(f"Retrieval failed: {e}")
# # # #         return f"Error during retrieval: {str(e)}"

# # # # # -----------------------------
# # # # # Agent
# # # # # -----------------------------
# # # # agent = Agent(
# # # #     name="Physical AI Tutor",
# # # #     instructions="""
# # # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # # To answer the user question, first call the tool `retrieve` with the user query.
# # # # Use ONLY the returned content from `retrieve` to answer.
# # # # If the answer is not in the retrieved content, say "I don't know".
# # # # Be clear, concise, and educational in your responses.
# # # # """,
# # # #     model=model,
# # # #     tools=[retrieve],
# # # # )

# # # # # -----------------------------
# # # # # Service Class
# # # # # -----------------------------
# # # # class ChatbotService:
# # # #     """Full async RAG pipeline for Physical AI chatbot"""

# # # #     async def process_chat(
# # # #         self, 
# # # #         query: str, 
# # # #         selected_text: str = None, 
# # # #         conversation_id: str | None = None
# # # #     ) -> Dict[str, Any]:
# # # #         """
# # # #         Process a chat query using RAG pipeline
        
# # # #         Args:
# # # #             query: User's question
# # # #             selected_text: Optional context from selected text
# # # #             conversation_id: Optional conversation identifier
            
# # # #         Returns:
# # # #             Dict containing response, conversation_id, and sources
# # # #         """
# # # #         conversation_id = conversation_id or "default_conversation"
# # # #         full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # # #         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# # # #         try:
# # # #             # Run the agent
# # # #             result = await Runner.run(agent, input=full_query)
            
# # # #             # Extract the final output
# # # #             response_text = getattr(result, "final_output", "I don't know")
            
# # # #             # Extract sources from tool calls if available
# # # #             sources = []
# # # #             tool_calls = getattr(result, "tool_calls", [])
# # # #             for call in tool_calls:
# # # #                 output = getattr(call, "output", None)
# # # #                 if output and isinstance(output, list):
# # # #                     for item in output:
# # # #                         if isinstance(item, dict) and "url" in item:
# # # #                             sources.append(item["url"])
            
# # # #             logger.info(f"Conversation [{conversation_id}] - Response generated successfully")
            
# # # #             return {
# # # #                 "response": response_text,
# # # #                 "conversation_id": conversation_id,
# # # #                 "sources": sources[:5]
# # # #             }

# # # #         except Exception as e:
# # # #             logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
# # # #             return {
# # # #                 "response": "An internal error occurred. Please try again.",
# # # #                 "conversation_id": conversation_id,
# # # #                 "sources": []
# # # #             }

# # # # # -----------------------------
# # # # # Global instance
# # # # # -----------------------------
# # # # chatbot_service = ChatbotService()


# # # import os
# # # from typing import List, Dict, Any
# # # from dotenv import load_dotenv
# # # import cohere
# # # from qdrant_client import QdrantClient
# # # from qdrant_client.models import Filter, PointStruct
# # # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # # from ..core.config import settings
# # # from ..core.logging import logger

# # # load_dotenv()
# # # enable_verbose_stdout_logging()
# # # set_tracing_disabled(disabled=True)

# # # # -----------------------------
# # # # Cohere Embeddings
# # # # -----------------------------
# # # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # # if not cohere_api_key:
# # #     raise ValueError("COHERE_API_KEY is required")
# # # cohere_client = cohere.Client(cohere_api_key)

# # # # -----------------------------
# # # # Qdrant Setup
# # # # -----------------------------
# # # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # # if not qdrant_url:
# # #     raise ValueError("QDRANT_URL is required")

# # # # Initialize Qdrant client
# # # try:
# # #     qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
# # #     # Test connection
# # #     collections = qdrant.get_collections()
# # #     logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
# # # except Exception as e:
# # #     logger.error(f"Failed to connect to Qdrant: {e}")
# # #     raise

# # # # -----------------------------
# # # # Groq LLM Setup
# # # # -----------------------------
# # # groq_api_key = os.getenv("GROQ_API_KEY")
# # # if not groq_api_key:
# # #     raise ValueError("GROQ_API_KEY is required")

# # # provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# # # # Fixed: Use the current supported model (replacement for the decommissioned llama-3.1-70b-versatile)
# # # model = OpenAIChatCompletionsModel(
# # #     model="llama-3.3-70b-versatile",
# # #     openai_client=provider
# # # )

# # # # -----------------------------
# # # # Embedding + Retrieval Tools
# # # # -----------------------------
# # # async def get_embedding(text: str) -> List[float]:
# # #     """Generate embedding using Cohere"""
# # #     try:
# # #         response = cohere_client.embed(
# # #             model=settings.EMBED_MODEL or "embed-english-v3.0",
# # #             input_type="search_query",
# # #             texts=[text]
# # #         )
# # #         return response.embeddings[0]
# # #     except Exception as e:
# # #         logger.error(f"Embedding generation failed: {e}")
# # #         raise

# # # @function_tool
# # # async def retrieve(query: str) -> str:
# # #     """Retrieve relevant documents from Qdrant vector database
    
# # #     Args:
# # #         query: The search query string
        
# # #     Returns:
# # #         A string containing the retrieved information
# # #     """
# # #     try:
# # #         # Generate embedding for the query
# # #         embedding = await get_embedding(query)
# # #         logger.info(f"Generated embedding for query: {query}")
        
# # #         # Search in Qdrant
# # #         search_result = qdrant.search(
# # #             collection_name="physical-ai-humanoid_robotics_book",
# # #             query_vector=embedding,
# # #             limit=5
# # #         )
        
# # #         logger.info(f"Retrieved {len(search_result)} results from Qdrant")
        
# # #         # Extract text from payloads and combine
# # #         texts = []
# # #         for point in search_result:
# # #             if point.payload and "text" in point.payload:
# # #                 texts.append(point.payload["text"])
        
# # #         if texts:
# # #             # Return combined text with separators
# # #             return "\n\n---\n\n".join(texts)
# # #         else:
# # #             return "No relevant information found in the knowledge base."
        
# # #     except Exception as e:
# # #         logger.error(f"Retrieval failed: {e}")
# # #         return f"Error during retrieval: {str(e)}"

# # # # -----------------------------
# # # # Agent
# # # # -----------------------------
# # # agent = Agent(
# # #     name="Physical AI Tutor",
# # #     instructions="""
# # # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # # To answer the user question, first call the tool `retrieve` with the user query.
# # # Use ONLY the returned content from `retrieve` to answer.
# # # If the answer is not in the retrieved content, say "I don't know".
# # # Be clear, concise, and educational in your responses.
# # # """,
# # #     model=model,
# # #     tools=[retrieve],
# # # )

# # # # -----------------------------
# # # # Service Class
# # # # -----------------------------
# # # class ChatbotService:
# # #     """Full async RAG pipeline for Physical AI chatbot"""

# # #     async def process_chat(
# # #         self, 
# # #         query: str, 
# # #         selected_text: str = None, 
# # #         conversation_id: str | None = None
# # #     ) -> Dict[str, Any]:
# # #         """
# # #         Process a chat query using RAG pipeline
        
# # #         Args:
# # #             query: User's question
# # #             selected_text: Optional context from selected text
# # #             conversation_id: Optional conversation identifier
            
# # #         Returns:
# # #             Dict containing response, conversation_id, and sources
# # #         """
# # #         conversation_id = conversation_id or "default_conversation"
# # #         full_query = f"{selected_text}\n\n{query}" if selected_text else query
# # #         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# # #         try:
# # #             # Run the agent
# # #             result = await Runner.run(agent, input=full_query)
            
# # #             # Extract the final output
# # #             response_text = getattr(result, "final_output", "I don't know")
            
# # #             # Fixed: Properly collect sources (retrieved chunks)
# # #             sources = []
# # #             tool_calls = getattr(result, "tool_calls", [])
# # #             for i, call in enumerate(tool_calls, start=1):
# # #                 output = getattr(call, "output", None)
# # #                 if output and isinstance(output, str) and output.strip():
# # #                     sources.append(f"Source {i}: Retrieved passage from the textbook")

# # #             logger.info(f"Conversation [{conversation_id}] - Response generated successfully")
            
# # #             return {
# # #                 "response": response_text,
# # #                 "conversation_id": conversation_id,
# # #                 "sources": sources[:5]  # Limit to 5 sources
# # #             }

# # #         except Exception as e:
# # #             logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
# # #             return {
# # #                 "response": "An internal error occurred. Please try again.",
# # #                 "conversation_id": conversation_id,
# # #                 "sources": []
# # #             }

# # # # -----------------------------
# # # # Global instance
# # # # -----------------------------
# # # chatbot_service = ChatbotService()
# # import os
# # from typing import List, Dict, Any
# # from dotenv import load_dotenv
# # import cohere
# # from qdrant_client import QdrantClient
# # from qdrant_client.models import VectorParams, Distance  # For potential future use
# # from qdrant_client.models import QueryRequest  # New import for query API
# # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# # from ..core.config import settings
# # from ..core.logging import logger

# # load_dotenv()
# # enable_verbose_stdout_logging()
# # set_tracing_disabled(disabled=True)

# # # -----------------------------
# # # Cohere Embeddings
# # # -----------------------------
# # cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# # if not cohere_api_key:
# #     raise ValueError("COHERE_API_KEY is required")
# # cohere_client = cohere.Client(cohere_api_key)

# # # -----------------------------
# # # Qdrant Setup
# # # -----------------------------
# # qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# # qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# # if not qdrant_url:
# #     raise ValueError("QDRANT_URL is required")

# # try:
# #     qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
# #     collections = qdrant.get_collections()
# #     logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
# # except Exception as e:
# #     logger.error(f"Failed to connect to Qdrant: {e}")
# #     raise

# # # -----------------------------
# # # Groq LLM Setup
# # # -----------------------------
# # groq_api_key = os.getenv("GROQ_API_KEY")
# # if not groq_api_key:
# #     raise ValueError("GROQ_API_KEY is required")

# # provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# # model = OpenAIChatCompletionsModel(
# #     model="llama-3.3-70b-versatile",  # Current, supported, great tool calling
# #     openai_client=provider
# # )

# # # -----------------------------
# # # Embedding + Retrieval Tools
# # # -----------------------------
# # async def get_embedding(text: str) -> List[float]:
# #     try:
# #         response = cohere_client.embed(
# #             model=settings.EMBED_MODEL or "embed-english-v3.0",
# #             input_type="search_query",
# #             texts=[text]
# #         )
# #         return response.embeddings[0]
# #     except Exception as e:
# #         logger.error(f"Embedding generation failed: {e}")
# #         raise

# # @function_tool
# # async def retrieve(query: str) -> str:
# #     """Retrieve relevant documents from Qdrant vector database
    
# #     Args:
# #         query: The search query string
        
# #     Returns:
# #         A string containing the retrieved information
# #     """
# #     try:
# #         embedding = await get_embedding(query)
# #         logger.info(f"Generated embedding for query: {query}")
        
# #         # NEW: Use the modern Query API instead of deprecated .search()
# #         search_result = qdrant.query_points(
# #             collection_name="physical-ai-humanoid_robotics_book",
# #             query=embedding,  # Direct vector query
# #             limit=5,
# #             with_payload=True,  # Ensure payload (text) is returned
# #         ).points
        
# #         logger.info(f"Retrieved {len(search_result)} results from Qdrant")
        
# #         texts = []
# #         for point in search_result:
# #             if point.payload and "text" in point.payload:
# #                 texts.append(point.payload["text"])
        
# #         if texts:
# #             return "\n\n---\n\n".join(texts)
# #         else:
# #             return "No relevant information found in the knowledge base."
        
# #     except Exception as e:
# #         logger.error(f"Retrieval failed: {e}")
# #         return f"Error during retrieval: {str(e)}"

# # # -----------------------------
# # # Agent
# # # -----------------------------
# # agent = Agent(
# #     name="Physical AI Tutor",
# #     instructions="""
# # You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
# # To answer the user question, first call the tool `retrieve` with the user query.
# # Use ONLY the returned content from `retrieve` to answer.
# # If the answer is not in the retrieved content, say "I don't know".
# # Be clear, concise, and educational in your responses.
# # """,
# #     model=model,
# #     tools=[retrieve],
# # )

# # # -----------------------------
# # # Service Class
# # # -----------------------------
# # class ChatbotService:
# #     """Full async RAG pipeline for Physical AI chatbot"""

# #     async def process_chat(
# #         self, 
# #         query: str, 
# #         selected_text: str = None, 
# #         conversation_id: str | None = None
# #     ) -> Dict[str, Any]:
# #         conversation_id = conversation_id or "default_conversation"
# #         full_query = f"{selected_text}\n\n{query}" if selected_text else query
# #         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

# #         try:
# #             result = await Runner.run(agent, input=full_query)
# #             response_text = getattr(result, "final_output", "I don't know")
            
# #             # Improved sources: Show a preview snippet from each retrieved chunk
# #             sources = []
# #             tool_calls = getattr(result, "tool_calls", [])
# #             for i, call in enumerate(tool_calls, start=1):
# #                 output = getattr(call, "output", None)
# #                 if output and isinstance(output, str) and output.strip() and "Error" not in output:
# #                     preview = output.strip().split("\n")[0][:200] + "..." if len(output) > 200 else output.strip()
# #                     sources.append(f"Source {i}: {preview}")

# #             logger.info(f"Conversation [{conversation_id}] - Response generated successfully")
            
# #             return {
# #                 "response": response_text,
# #                 "conversation_id": conversation_id,
# #                 "sources": sources[:5]
# #             }

# #         except Exception as e:
# #             logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
# #             return {
# #                 "response": "An internal error occurred. Please try again.",
# #                 "conversation_id": conversation_id,
# #                 "sources": []
# #             }

# # # -----------------------------
# # # Global instance
# # # -----------------------------
# # chatbot_service = ChatbotService()

# import os
# from typing import List, Dict, Any
# from dotenv import load_dotenv
# import cohere
# from qdrant_client import QdrantClient
# from qdrant_client.models import NearestQuery  # Import for vector query
# from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
# from ..core.config import settings
# from ..core.logging import logger

# load_dotenv()
# enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)

# # -----------------------------
# # Cohere Embeddings
# # -----------------------------
# cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
# if not cohere_api_key:
#     raise ValueError("COHERE_API_KEY is required")
# cohere_client = cohere.Client(cohere_api_key)

# # -----------------------------
# # Qdrant Setup
# # -----------------------------
# qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
# qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
# if not qdrant_url:
#     raise ValueError("QDRANT_URL is required")

# try:
#     qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
#     collections = qdrant.get_collections()
#     logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
# except Exception as e:
#     logger.error(f"Failed to connect to Qdrant: {e}")
#     raise

# # -----------------------------
# # Groq LLM Setup - FIXED: Use dedicated tool-use model
# # -----------------------------
# groq_api_key = os.getenv("GROQ_API_KEY")
# if not groq_api_key:
#     raise ValueError("GROQ_API_KEY is required")

# provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")

# # BEST FIX: Use the specialized tool-use model for reliable function calling
# model = OpenAIChatCompletionsModel(
#     model="llama3-groq-70b-8192-tool-use-preview",
#     openai_client=provider
# )

# # -----------------------------
# # Embedding + Retrieval Tools
# # -----------------------------
# async def get_embedding(text: str) -> List[float]:
#     try:
#         response = cohere_client.embed(
#             model=settings.EMBED_MODEL or "embed-english-v3.0",
#             input_type="search_query",
#             texts=[text]
#         )
#         return response.embeddings[0]
#     except Exception as e:
#         logger.error(f"Embedding generation failed: {e}")
#         raise

# @function_tool
# async def retrieve(query: str) -> str:
#     """Retrieve relevant documents from Qdrant vector database
    
#     Args:
#         query: The search query string
        
#     Returns:
#         A string containing the retrieved information
#     """
#     try:
#         embedding = await get_embedding(query)
#         logger.info(f"Generated embedding for query: {query}")
        
#         # FIXED: Use correct modern Qdrant API - NearestQuery for vector search
#         search_result = qdrant.query_points(
#             collection_name="physical-ai-humanoid_robotics_book",
#             query=NearestQuery(nearest=embedding),
#             limit=5,
#             with_payload=True,
#         ).points
        
#         logger.info(f"Retrieved {len(search_result)} results from Qdrant")
        
#         texts = []
#         for point in search_result:
#             if point.payload and "text" in point.payload:
#                 texts.append(point.payload["text"])
        
#         if texts:
#             return "\n\n---\n\n".join(texts)
#         else:
#             return "No relevant information found in the knowledge base."
        
#     except Exception as e:
#         logger.error(f"Retrieval failed: {e}")
#         return f"Error during retrieval: {str(e)}"

# # -----------------------------
# # Agent - Improved instructions for better tool use
# # -----------------------------
# agent = Agent(
#     name="Physical AI Tutor",
#     instructions="""
# You are an expert tutor for the Physical AI & Humanoid Robotics textbook.
# Answer questions using ONLY the information retrieved from the `retrieve` tool.
# First, ALWAYS call the `retrieve` tool with a precise query based on the user's question.
# Then, use the returned content to give a clear, concise, and educational answer.
# If no relevant information is found, respond: "I don't know based on the textbook."
# """,
#     model=model,
#     tools=[retrieve],
# )

# # -----------------------------
# # Service Class
# # -----------------------------
# class ChatbotService:
#     async def process_chat(
#         self, 
#         query: str, 
#         selected_text: str = None, 
#         conversation_id: str | None = None
#     ) -> Dict[str, Any]:
#         conversation_id = conversation_id or "default_conversation"
#         full_query = f"{selected_text}\n\n{query}" if selected_text else query
#         logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

#         try:
#             result = await Runner.run(agent, input=full_query)
#             response_text = getattr(result, "final_output", "I don't know")
            
#             # Better source previews
#             sources = []
#             tool_calls = getattr(result, "tool_calls", [])
#             for i, call in enumerate(tool_calls, start=1):
#                 output = getattr(call, "output", None)
#                 if output and isinstance(output, str) and "Error" not in output and output.strip():
#                     preview = output.strip().split("\n", 1)[0][:150] + "..." if len(output) > 150 else output.strip()
#                     sources.append(f"Source {i}: {preview}")

#             logger.info(f"Conversation [{conversation_id}] - Response generated successfully")
            
#             return {
#                 "response": response_text,
#                 "conversation_id": conversation_id,
#                 "sources": sources[:5]
#             }

#         except Exception as e:
#             logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
#             return {
#                 "response": "An internal error occurred. Please try again.",
#                 "conversation_id": conversation_id,
#                 "sources": []
#             }

# # -----------------------------
# # Global instance
# # -----------------------------
# chatbot_service = ChatbotService()

import os
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import NearestQuery
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, enable_verbose_stdout_logging
from agents.model_settings import ModelSettings
from ..core.config import settings
from ..core.logging import logger

load_dotenv()
enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)

# -----------------------------
# Cohere Embeddings
# -----------------------------
cohere_api_key = settings.COHERE_API_KEY or os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY is required")
cohere_client = cohere.Client(cohere_api_key)

# -----------------------------
# Qdrant Setup
# -----------------------------
qdrant_url = settings.QDRANT_URL or os.getenv("QDRANT_URL")
qdrant_api_key = settings.QDRANT_API_KEY or os.getenv("QDRANT_API_KEY")
if not qdrant_url:
    raise ValueError("QDRANT_URL is required")

try:
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    collections = qdrant.get_collections()
    logger.info(f"Successfully connected to Qdrant. Collections: {len(collections.collections)}")
except Exception as e:
    logger.error(f"Failed to connect to Qdrant: {e}")
    raise

# -----------------------------
# OpenRouter LLM Setup
# -----------------------------
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is required")

provider = AsyncOpenAI(
    api_key=openrouter_api_key, 
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8000", # Aapki app ka URL
        "X-Title": "Physical AI Tutor",          # Aapki app ka naam
    }
)

# Using a reliable model that supports function calling on OpenRouter
model = OpenAIChatCompletionsModel(
    model="google/gemini-2.0-flash-001",  # Free model with strong tool calling support
    openai_client=provider,
)

# -----------------------------
# Embedding + Retrieval Tools
# -----------------------------
async def get_embedding(text: str, max_retries: int = 3) -> List[float]:
    """
    Generate embedding with retry logic for rate limiting

    Args:
        text: Text to embed
        max_retries: Maximum number of retry attempts

    Returns:
        List of float representing the embedding vector
    """
    for attempt in range(max_retries):
        try:
            response = cohere_client.embed(
                model=settings.EMBED_MODEL or "embed-english-v3.0",
                input_type="search_query",
                texts=[text]
            )
            return response.embeddings[0]
        except cohere.CohereAPIError as e:
            # Check if this is a rate limit error
            if hasattr(e, 'status_code') and e.status_code == 429:
                wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s...")
                if attempt < max_retries - 1:  # Don't wait on the last attempt
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limit exceeded after {max_retries} retries")
                    raise Exception("Cohere API rate limit exceeded. Please try again in a few seconds.")
            else:
                logger.error(f"Embedding generation failed: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error in embedding generation: {e}")
            raise

@function_tool
async def retrieve(query: str) -> str:
    """Retrieve relevant documents from Qdrant vector database"""
    try:
        # Generate embedding with retry logic
        embedding = await get_embedding(query)
        logger.info(f"Generated embedding for query: {query}")

        # Search in Qdrant
        search_result = qdrant.query_points(
            collection_name="physical-ai-humanoid_robotics_book1",
            query=NearestQuery(nearest=embedding),
            limit=5,
            with_payload=True,
         ).points

        logger.info(f"Retrieved {len(search_result)} results from Qdrant")

        # Extract text payloads
        texts = [point.payload["text"] for point in search_result if point.payload and "text" in point.payload]

        if texts:
            return "\n\n---\n\n".join(texts)
        else:
            return "No relevant information found in the knowledge base."

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Retrieval failed: {error_msg}")

        # Provide user-friendly error messages
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            return "The system is experiencing high load. Please wait a moment and try again."
        elif "timeout" in error_msg.lower():
            return "The search took too long. Please try rephrasing your question."
        else:
            return "Unable to search the knowledge base. Please try again."

# -----------------------------
# Agent - Strong instructions + forced tool use
# -----------------------------
agent = Agent(
    name="Physical AI Tutor",
    instructions="""
You are "Physical AI Tutor", an expert tutor for the textbook
"Physical AI & Humanoid Robotics".

════════════════════════════════════
ROLE & IDENTITY
════════════════════════════════════
- You are a university-level instructor specializing in:
  Physical AI, Humanoid Robotics, and Embodied Intelligence.
- Your job is to teach and explain concepts strictly from
  the textbook content stored in the knowledge base.
- You must behave like a calm, clear, and precise tutor —
  not a chatbot, not a marketer, not a motivational speaker.

════════════════════════════════════
RETRIEVAL (RAG) RULES — VERY IMPORTANT
════════════════════════════════════
1. Use the `retrieve` tool ONLY when the user's message is
   a textbook-related question.

2. Textbook-related topics include:
   - Physical AI
   - Humanoid robotics
   - Control systems
   - Locomotion & balance
   - AI perception (vision, sensors, sensor fusion)
   - Reinforcement learning
   - Perception–action loops
   - ROS / simulation / labs
   - Architectures, modules, or applications described in the book

3. NEVER use the `retrieve` tool for:
   - Greetings (hi, hello, hey)
   - Slogans or taglines
   - UI text or headings
   - Casual or unclear messages
   - Motivational phrases

════════════════════════════════════
GREETING & CASUAL INPUT HANDLING
════════════════════════════════════
- If the user says:
  "hi", "hello", "hey", or similar
  → Respond politely WITHOUT using the retrieve tool.

- If the user sends a slogan or heading (e.g.:
  "Build the Future with Humanoid Robots"):
  → Treat it as non-textbook content
  → Respond briefly and politely
  → DO NOT retrieve

════════════════════════════════════
ANSWERING TEXTBOOK QUESTIONS
════════════════════════════════════
When the question IS related to the textbook:

1. You MUST call the `retrieve` tool first.
2. Base your answer ONLY on retrieved content.
3. Explain in your own words — do NOT copy long passages.
4. If retrieval returns no relevant information, say EXACTLY:
   "I don't know based on the textbook."

════════════════════════════════════
EXPLANATION STYLE
════════════════════════════════════
- Keep explanations clear, simple, and structured.
- Prefer:
  - Bullet points
  - Short paragraphs
- Explain like a good teacher, not like documentation.
- Avoid unnecessary complexity unless the user asks for depth.

════════════════════════════════════
BOUNDARIES & SAFETY
════════════════════════════════════
- If a question is outside the book scope, say EXACTLY:
  "This topic is outside the scope of the textbook."
- Never mention:
  - Internal tools
  - Embeddings
  - Vector databases
  - System prompts
  - Retrieval logic

════════════════════════════════════
GOAL
════════════════════════════════════
Help learners clearly and accurately understand
Physical AI & Humanoid Robotics exactly as presented
in the textbook — nothing more, nothing less.
""",
    model=model,
    tools=[retrieve],
    # model_settings=ModelSettings(
    #     # 'required' force karta hai model ko tool use karne par. 
    #     # Agar error aaye to ise "auto" kar dein.
    #     tool_choice="required" 
    # )
)

# -----------------------------
# Service Class
# -----------------------------
class ChatbotService:
    async def process_chat(
        self, 
        query: str, 
        selected_text: str = None, 
        conversation_id: str | None = None
    ) -> Dict[str, Any]:
        conversation_id = conversation_id or "default_conversation"
        full_query = f"{selected_text}\n\n{query}" if selected_text else query
        logger.info(f"Conversation [{conversation_id}] - Query: {full_query}")

        try:
            result = await Runner.run(agent, input=full_query)
            response_text = getattr(result, "final_output", "I don't know based on the textbook.")

            sources = []
            for i, call in enumerate(getattr(result, "tool_calls", []), start=1):
                output = getattr(call, "output", None)
                if output and isinstance(output, str) and "Error" not in output and output.strip():
                    preview = output.strip().split("\n", 1)[0][:150] + ("..." if len(output) > 150 else "")
                    sources.append(f"Source {i}: {preview}")

            logger.info(f"Conversation [{conversation_id}] - Response generated successfully")

            return {
                "response": response_text,
                "conversation_id": conversation_id,
                "sources": sources[:5]
                }

        except Exception as e:
            logger.exception(f"Chat processing failed for conversation [{conversation_id}]: {e}")
            return {
                "response": "An internal error occurred. Please try again.",
                "conversation_id": conversation_id,
                "sources": []
                }

chatbot_service = ChatbotService()