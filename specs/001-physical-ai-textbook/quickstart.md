# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites
- Node.js 18+
- Python 3.11+
- Git
- Access to OpenAI API
- Access to Qdrant Cloud
- Access to Neon Postgres

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd physical-ai-humanoid-robotics
```

### 2. Setup Frontend (Docusaurus)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (See Environment Variables section below)
```

### 3. Setup Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (See Environment Variables section below)
```

### 4. Environment Variables

#### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_OPENAI_API_KEY=your_openai_key_here
```

#### Backend (.env)
```
DATABASE_URL=your_neon_postgres_url
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key_for_auth
BETTER_AUTH_SECRET=your_better_auth_secret
```

### 5. Initialize the Database
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.utils.init_db
```

### 6. Index Textbook Content for RAG
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.utils.content_indexer
```

### 7. Run the Applications

#### Run Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m src.main
```
Backend will start on http://localhost:8000

#### Run Frontend Server
```bash
cd frontend
npm start
```
Frontend will start on http://localhost:3000

## API Endpoints

### RAG Chatbot
- `POST /api/chatbot/query` - Query the textbook content
- Request: `{ "query": "your question here" }`
- Response: `{ "answer": "answer from textbook", "sources": ["chapter1", "chapter2"] }`

### User Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile

### Personalization
- `POST /api/personalization/settings` - Update user preferences
- `GET /api/personalization/recommendations` - Get content recommendations

### Translation
- `POST /api/translation/toggle` - Toggle content language
- `GET /api/translation/available` - Get available languages

## Development Commands

### Frontend
```bash
# Run in development mode
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Backend
```bash
# Run with auto-reload
python -m src.main --reload

# Run tests
python -m pytest

# Format code
black src/
```

## Folder Structure
```
physical-ai-humanoid-robotics/
├── frontend/                 # Docusaurus application
│   ├── docs/                # Textbook chapters
│   ├── src/                 # Custom React components
│   ├── static/              # Images and assets
│   └── docusaurus.config.js # Docusaurus configuration
├── backend/                  # FastAPI application
│   ├── src/
│   │   ├── models/          # Data models
│   │   ├── services/        # Business logic
│   │   ├── api/             # API routes
│   │   └── utils/           # Utility functions
│   └── tests/               # Test files
└── scripts/                  # Deployment and utility scripts
```

## Troubleshooting

### Common Issues
1. **Port already in use**: Change ports in configuration files
2. **Database connection fails**: Verify DATABASE_URL in backend .env
3. **API keys not working**: Double-check all API keys in environment files
4. **Content not indexing**: Ensure the content files exist in docs/ directory

### Verification Steps
1. Check that both frontend and backend servers are running
2. Visit http://localhost:3000 to access the textbook
3. Test the chatbot functionality with a sample question
4. Verify user registration and login work correctly