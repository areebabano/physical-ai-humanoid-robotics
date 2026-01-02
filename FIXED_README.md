# Physical AI & Humanoid Robotics - Fixed RAG Chatbot System

This project has been fixed to resolve port conflicts and other issues between frontend and backend services.

## Issues Fixed

### 1. Port Conflict Resolution
- **Before**: Both frontend and backend running on port 8000
- **After**:
  - Backend runs on **port 8000**
  - Frontend runs on **port 3000**

### 2. CORS Configuration
- Backend properly configured with CORS to allow frontend origin
- Wildcard (*) allowed for development
- Proper headers exposed for client access

### 3. WebSocket Support Added
- New WebSocket endpoint at `/ws` for real-time chat
- Connection manager with auto-reconnection
- Ping/pong heartbeat mechanism
- Fallback to REST API if WebSocket unavailable

### 4. ChatbotWidget Updates
- **ChatbotWidget.jsx**: Updated with WebSocket support
- **ChatbotWidget.tsx**: Updated with WebSocket support
- Connection status indicator (WS/API)
- Auto-fallback to REST API when WebSocket unavailable
- Improved error handling and loading states

### 5. Environment Configuration
- Updated `.env.example` with correct settings
- Proper API model names for Gemini
- SQLite database configuration
- Local Qdrant configuration

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   Vector DB     │
│  (Port 3000)    │───▶│   (Port 8000)    │───▶│  (Port 6333)    │
│                 │    │                  │    │                 │
│ Docusaurus      │    │ FastAPI          │    │ Qdrant          │
│ React Widget    │    │ WebSockets/REST  │    │ Docker          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Services

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| Frontend | 3000 | `http://localhost:3000` | Docusaurus documentation site |
| Backend | 8000 | `http://localhost:8000` | FastAPI REST API |
| WebSocket | 8000 | `ws://localhost:8000/ws` | Real-time chat |
| Qdrant | 6333 | `http://localhost:6333` | Vector database |

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 18+
- Docker Desktop
- Git

### 1. Automatic Setup (Recommended)
Run the complete setup script:
```bash
complete_setup.bat
```

This script will:
- Check all prerequisites
- Start Qdrant Docker container
- Start backend on port 8000
- Start frontend on port 3000
- Verify all services are running

### 2. Manual Setup

#### A. Start Qdrant (Vector Database)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

#### B. Start Backend Server
```bash
cd "D:\AI Book\physical-ai-humanoid-robotics"
python run_server.py
# OR
cd "D:\AI Book\physical-ai-humanoid-robotics\backend"
uvicorn src.main:app --reload --port 8000
```

#### C. Start Frontend Server
```bash
cd "D:\AI Book\physical-ai-humanoid-robotics"
npx docusaurus start --port 3000
```

## WebSocket Features

The chatbot now supports real-time communication via WebSocket:

### Connection Status
- Green dot: WebSocket connected
- Red dot: Using fallback REST API
- Shows "WS" when connected, "API" when using fallback

### WebSocket Endpoint
- URL: `ws://localhost:8000/ws`
- Supports ping/pong for connection health
- Auto-reconnection every 3 seconds if disconnected
- Message types: `chat`, `ping`, `echo`

## API Endpoints

### REST API
- `GET /health` - Health check
- `POST /api/chatbot/chat` - Chat with RAG
- `POST /api/chatbot/ingest` - Ingest content
- `GET /api/chatbot/health` - Chatbot health

### WebSocket API
- `ws://localhost:8000/ws` - Real-time chat
- Message format: `{"type": "chat", "content": "message", "selected_text": "text"}`
- Response format: `{"type": "chat_response", "content": "response", "sources": [...]}`

## Configuration

### Environment Variables (.env)
```env
# Backend Configuration
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_CHAT_MODEL=models/gemini-1.5-flash
GEMINI_EMBEDDING_MODEL=models/text-embedding-004

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=textbook_content

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./textbook.db

# Security
JWT_SECRET_KEY=your_generated_secret_key
PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Check for existing processes: `netstat -ano | findstr :8000`
   - Kill processes if needed: `taskkill /f /pid <PID>`

2. **Docker Not Starting**
   - Ensure Docker Desktop is running
   - Restart Docker Desktop if needed
   - Check system resources

3. **WebSocket Connection Failing**
   - Verify backend is running on port 8000
   - Check firewall settings
   - Ensure no proxy is blocking WebSocket connections

4. **CORS Errors**
   - Verify ALLOWED_ORIGINS in .env
   - Check that frontend is on port 3000
   - Ensure backend CORS settings are correct

### Verification Commands

Check if services are running:
```bash
# Backend
curl http://localhost:8000/health

# Qdrant
curl http://localhost:6333/health

# Frontend
# Open http://localhost:3000 in browser
```

## Files Updated

### Backend
- `backend/src/main.py` - Added WebSocket support, improved CORS
- `backend/src/config.py` - Updated model names

### Frontend
- `src/components/ChatbotWidget/ChatbotWidget.jsx` - WebSocket integration
- `src/components/ChatbotWidget/ChatbotWidget.tsx` - WebSocket integration
- `src/components/ChatbotWidget/ChatbotWidget.css` - Connection status styles

### Scripts
- `complete_setup.bat` - Complete setup script
- `start_rag_system.bat` - Alternative startup script
- `run_both_servers.bat` - Port-separated startup

The system is now fully functional with proper port separation, WebSocket support, and resolved CORS issues!