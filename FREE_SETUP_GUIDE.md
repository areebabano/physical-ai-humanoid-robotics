# 100% Free Setup Guide for Physical AI & Humanoid Robotics Textbook RAG Chatbot

This guide will help you set up the RAG chatbot system using completely free services.

## Step 1: Get Free Gemini API Key

1. Go to https://aistudio.google.com/
2. Sign in with your Google account
3. Click on "Get API Key" or "Create API Key"
4. **Important**: Do NOT add billing/credit card - the free tier is sufficient for this project
5. Copy your API key (format: `AIzaSyXXXXXXXX`)

## Step 2: Configure Environment Variables

Create a `.env` file in the project root with these settings:

```bash
# Gemini API Configuration (FREE - Get from https://aistudio.google.com)
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_CHAT_MODEL=models/gemini-1.5-flash
GEMINI_EMBEDDING_MODEL=models/text-embedding-004

# Qdrant Vector Database Configuration (FREE - Local Docker)
# Install Docker from https://www.docker.com/
# Run: docker run -p 6333:6333 qdrant/qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=textbook_content

# Database Configuration (FREE - SQLite)
DATABASE_URL=sqlite+aiosqlite:///./textbook.db

# Authentication
# Generate JWT secret: python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY=your_generated_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Configuration
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_HOUR=50

# Logging
LOG_LEVEL=INFO

# Development/Production Mode
ENVIRONMENT=development

# Vector Database Configuration
VECTOR_DIMENSION=768
```

## Step 3: Generate JWT Secret Key

Run this command in your terminal to generate a secure JWT secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `JWT_SECRET_KEY`.

## Step 4: Set Up Local Qdrant (Vector Database)

### Option A: Using Docker (Recommended)
1. Install Docker from https://www.docker.com/
2. Run this command in your terminal:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Option B: Using Docker Compose
Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
volumes:
  qdrant_data:
```

Then run:
```bash
docker-compose up -d
```

## Step 5: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 6: Run the Application

### Terminal 1: Start the Qdrant Vector Database
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Terminal 2: Start the Backend Server
```bash
cd backend
python run_server.py
# Or alternatively:
uvicorn src.main:app --reload --port 8000
```

### Terminal 3: Start the Docusaurus Frontend (if applicable)
```bash
cd /path/to/your/docusaurus
npm start
```

## Step 7: Ingest Textbook Content

To populate the vector database with your textbook content, you can use the ingestion API:

```bash
curl -X POST http://localhost:8000/api/chatbot/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your textbook content here...",
    "source": "chapter_1.md",
    "target": "all"
  }'
```

## Step 8: Test the Chatbot

Visit your Docusaurus site and test the chatbot widget. You can also test the API directly:

```bash
curl -X POST http://localhost:8000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is physical AI?",
    "selected_text": null
  }'
```

## Free Tier Limits & Considerations

- **Gemini API**: Free tier has usage limits (check Google AI Studio for current limits)
- **Qdrant**: Local Docker instance has no limits
- **SQLite**: Local database with no limits
- **Rate Limiting**: Configured to 50 requests/hour to respect API limits

## Troubleshooting

### Qdrant Connection Issues
- Ensure Docker is running
- Verify Qdrant is accessible at http://localhost:6333
- Check the Qdrant container logs: `docker logs <container_id>`

### API Key Issues
- Verify your Gemini API key is correct
- Check that you haven't exceeded your free tier limits
- Ensure the model names are correct (`models/gemini-1.5-flash`, `models/text-embedding-004`)

### Database Issues
- Make sure the SQLite file path is correct
- Ensure the application has write permissions to the directory

## Benefits of This Free Setup

✅ 100% free to run and maintain
✅ No credit card required
✅ Perfect for assignments and demos
✅ Local vector database for privacy
✅ No external dependencies beyond Gemini API
✅ Full control over your data

This setup allows you to run a complete RAG chatbot system without any recurring costs!