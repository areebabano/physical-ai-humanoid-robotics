# RAG Chatbot Setup Instructions

## Prerequisites

1. **Python 3.11+** - Required for backend services
2. **Node.js 18+** - Required for frontend development
3. **Docker** - Required for Qdrant vector database
4. **Ollama** - Required for free LLM models (or compatible API)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Update the `.env` file with your specific configuration:

```bash
# Edit the .env file to match your environment
nano .env
```

### 3. Install and Run Qdrant

Using Docker:

```bash
# Pull and run Qdrant container
docker run -p 6333:6333 -p 6334:6334 \
    -e QDRANT_API_KEY=your-api-key-here \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### 4. Install and Run Ollama

For local free LLM models:

```bash
# Install Ollama (visit https://ollama.ai for installation)
# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Run the Backend Server

```bash
# From the backend directory
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd frontend  # or wherever your Docusaurus project is
npm install
```

### 2. Run the Frontend

```bash
npm start
```

## Integration with Docusaurus

### 1. Add Chatbot to Docusaurus

To embed the chatbot in your Docusaurus site, add the following to your Docusaurus configuration:

1. Install the chatbot component:
```bash
# If using as a component in Docusaurus
npm install path-to-chatbot-component
```

2. Add to your layout or specific pages:
```jsx
import ChatbotWidget from './path/to/ChatbotWidget';

function Layout({children}) {
  return (
    <>
      <main>{children}</main>
      <ChatbotWidget />
    </>
  );
}
```

### 2. Text Selection Feature

The chatbot automatically detects text selection on the page. When users select text and open the chat, the selected text will be used as context.

## Configuration Options

### Environment Variables Explained

- `QDRANT_URL`: URL for your Qdrant instance (default: http://localhost:6333)
- `FREE_LLM_BASE_URL`: Base URL for your LLM API (default: http://localhost:11434/api for Ollama)
- `FREE_LLM_MODEL_NAME`: Model name for chat responses (default: llama3.2)
- `FREE_LLM_EMBEDDING_MODEL`: Model name for embeddings (default: nomic-embed-text)
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per time window
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 3600 for 1 hour)

### Model Options

You can use various free models with this setup:

- **Llama 3.2** - Good general-purpose model
- **Mistral** - Alternative smaller model
- **Gemma** - Google's open model
- **Nomic Embed** - For text embeddings

## API Endpoints

### Chat Endpoint
```
POST /api/chatbot/chat
```

Request body:
```json
{
  "message": "Your question here",
  "selected_text": "Optional selected text for context",
  "conversation_id": "Optional conversation ID"
}
```

### Ingest Endpoint
```
POST /api/chatbot/ingest
```

Request body:
```json
{
  "content": "Content to index",
  "source": "Source identifier",
  "target": "all|module|file",
  "path": "Optional path for specific target"
}
```

## Testing the Setup

### 1. Health Check

Verify the backend is running:
```bash
curl http://localhost:8000/health
```

### 2. Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?",
    "selected_text": null
  }'
```

### 3. WebSocket Connection

The chatbot uses WebSocket for real-time communication:
```
ws://localhost:8000/ws
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Issues**
   - Verify Qdrant is running: `docker ps | grep qdrant`
   - Check the URL in your environment variables

2. **LLM Model Not Found**
   - Ensure models are pulled: `ollama list`
   - Check model names in environment variables

3. **CORS Issues**
   - Verify `ALLOWED_ORIGINS` in your environment
   - Check that frontend URL matches allowed origins

4. **Rate Limiting**
   - Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW` as needed
   - Monitor logs for rate limit messages

### Development Mode

For development, you can run with auto-reload:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

### Backend

1. Use a production database (PostgreSQL recommended)
2. Set `ENVIRONMENT=production` in your environment
3. Configure proper authentication and security settings
4. Use a reverse proxy (nginx) in front of the API

### Frontend

1. Build for production: `npm run build`
2. Serve the static files through your web server
3. Configure proper CORS settings

## Security Considerations

1. Never commit API keys to version control
2. Use environment variables for sensitive data
3. Implement proper rate limiting
4. Validate all user inputs
5. Use HTTPS in production