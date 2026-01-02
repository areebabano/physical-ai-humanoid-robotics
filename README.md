# Physical AI & Humanoid Robotics RAG Chatbot

A complete RAG (Retrieval-Augmented Generation) chatbot system for the Physical AI & Humanoid Robotics textbook using Cohere embeddings and language models.

## Features

- **RAG Chatbot**: Answers questions based on the textbook content using retrieval-augmented generation
- **Content Ingestion**: Automated ingestion from sitemap with text extraction and chunking
- **Vector Search**: Uses Qdrant for efficient semantic search of textbook content
- **Cohere Integration**: Uses Cohere's embed-english-v3.0 for embeddings and command-r-plus for responses
- **Modern UI**: Floating chatbot widget with draggable interface and smooth animations
- **WebSocket Support**: Real-time chat with WebSocket connections for instant responses
- **Source Attribution**: Shows source URLs for retrieved content in responses
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Robust error handling and fallback responses
- **Draggable Interface**: Chat window can be moved around the screen

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   FastAPI        │    │    External      │
│   Application   │◄──►│   Backend        │◄──►│    Services      │
│                 │    │                  │    │                  │
│  ┌─────────────┐│    │ ┌───────────────┐│    │ ┌──────────────┐ │
│  │Chatbot      ││    │ │RAG Chatbot   ││    │ │Qdrant        │ │
│  │Widget       ││    │ │Service        ││    │ │Vector DB     │ │
│  └─────────────┘│    │ └───────────────┘│    │ └──────────────┘ │
└─────────────────┘    └──────────────────┘    │ ┌──────────────┐ │
                                              │ │Cohere        │ │
                                              │ │Embed API     │ │
                                              │ │(embed-english-│ │
                                              │ │v3.0)         │ │
                                              │ └──────────────┘ │
                                              │ ┌──────────────┐ │
                                              │ │Cohere        │ │
                                              │ │Generate API  │ │
                                              │ │(command-r-plus│ │
                                              │ │)             │ │
                                              │ └──────────────┘ │
                                              └──────────────────┘
```

## Prerequisites

- Python 3.11+
- Cohere API Key
- Qdrant Cloud account
- (Optional) Node.js 18+ if modifying the frontend

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
# Create .env file in root directory
touch .env
```

5. Update the `.env` file with your credentials:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
SITEMAP_URL=https://your-website.com/sitemap.xml
INGESTION_COLLECTION_NAME=physical-ai-humanoid_robotics_book
```

6. Start the backend server:
```bash
python run_server.py
# Or directly:
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Content Ingestion

Run the content ingestion to populate the vector database:

```bash
python content_ingestion.py
```

This will fetch all URLs from your sitemap, extract text content, chunk it, generate embeddings, and store in Qdrant.

## API Endpoints

### Chatbot Endpoints

- `POST /api/chatbot/chat` - Process chat messages with RAG
- `GET /health` - Health check for the service
- `WS /ws` - WebSocket endpoint for real-time chat

### Request/Response Examples

**Chat Request:**
```json
{
  "message": "What is Physical AI?",
  "selected_text": "Optional selected text for additional context"
}
```

**Chat Response:**
```json
{
  "response": "Physical AI is an approach to robotics that emphasizes...",
  "conversation_id": "default_conversation",
  "sources": ["https://example.com/page1", "https://example.com/page2"]
}
```

## Testing

### Content Ingestion Test

Test the content ingestion process:
```bash
python content_ingestion.py
```

### Retrieval Test

Test the retrieval functionality:
```bash
python retrieval_test.py
```

### API Test

Test the chat API directly:
```bash
curl -X POST http://localhost:8000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?"
  }'
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection**: Check that your QDRANT_URL and QDRANT_API_KEY are valid
2. **Cohere API**: Confirm your COHERE_API_KEY is valid and has sufficient credits
3. **Sitemap Access**: Verify that your SITEMAP_URL is accessible and returns valid XML
4. **Port Conflicts**: Ensure port 8000 is available for the backend server
5. **Environment Variables**: Make sure all required environment variables are set

### Logging

The application logs to stdout. Check your terminal output for any errors.

## Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: React chatbot widget
- **Vector Database**: Qdrant Cloud
- **AI Models**: Cohere embed-english-v3.0 (embeddings), command-r-plus (generation)
- **Content Processing**: Trafilatura for text extraction
- **API Framework**: FastAPI with WebSocket support


## Security

- API keys are stored in environment variables
- CORS is configured to allow specified origins
- Input validation is performed on all API endpoints
- Secure connections (HTTPS) should be used in production
