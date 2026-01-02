# Physical AI Humanoid Robotics - Backend

This is the backend service for the Physical AI Humanoid Robotics textbook project. It provides a RAG (Retrieval Augmented Generation) system for querying the textbook content with both Google Gemini and Cohere integration.

## Features

- **RAG Question Answering**: Ask questions and get answers based on retrieved context
- **Google Gemini Integration**: Uses Gemini API for embeddings and chat
- **Cohere Integration**: Alternative embedding service using Cohere
- **Content Ingestion Pipeline**: Automated ingestion from sitemap
- **Qdrant Vector Database**: Stores and retrieves document embeddings
- **FastAPI**: Modern, fast web framework for building APIs
- **Environment Configuration**: All settings loaded from `.env` file
- **Health Check**: Endpoint to verify backend is running

## Requirements

- Python 3.8+
- Google Gemini API key
- Qdrant Cloud account or self-hosted instance

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration (see `.env.example`)

## Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Configuration
QDRANT_URL=https://your-qdrant-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=textbook_content

# Cohere Configuration (for alternative embedding service)
COHERE_API_KEY=your_cohere_api_key_here
EMBED_MODEL=embed-english-v3.0

# Content Ingestion Configuration
SITEMAP_URL=https://physical-ai-humanoid-robotics-khbj.vercel.app/sitemap.xml
INGESTION_COLLECTION_NAME=physical-ai-humanoid_robotics_book

# Model Configuration
GEMINI_EMBEDDING_MODEL=embedding-001
GEMINI_CHAT_MODEL=gemini-2.5-flash

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

Note: The backend is configured to use the free Google Gemini 2.5 Flash model for chat and embedding-001 for embeddings.

## Running the Server

```bash
python run_server.py
```

Or using uvicorn directly:

```bash
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Content Ingestion

To ingest content from the sitemap into the vector database:

```bash
python run_content_ingestion.py
```

This will:
1. Fetch URLs from the sitemap
2. Extract text content from each page
3. Chunk the text into manageable pieces
4. Generate embeddings using Cohere
5. Store the embeddings in Qdrant

## API Endpoints

### `/api/ask` - POST
Ask a question and get a response based on RAG.

**Request body:**
```json
{
  "question": "Your question here",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Generated answer based on context",
  "sources": ["source1", "source2"],
  "retrieved_chunks": [
    {
      "content": "retrieved content",
      "source": "source name",
      "module": "module name",
      "heading": "heading",
      "score": 0.8,
      "chunk_index": 0
    }
  ]
}
```

### `/api/health` - GET
Health check endpoint to verify the backend is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123
}
```

### Other Endpoints
The server also includes all the existing endpoints from the main application.

## How it Works

1. User submits a question via the `/api/ask` endpoint
2. The system generates an embedding for the question using Google Gemini
3. The embedding is used to search for similar content in Qdrant vector database
4. Top-k relevant chunks are retrieved from the vector database
5. The question and context are sent to Google Gemini to generate an answer
6. The answer is returned along with sources and retrieved chunks

## Error Handling

The system includes comprehensive error handling:
- API call timeouts
- Service unavailability
- Invalid requests
- Fallback responses when external services are down