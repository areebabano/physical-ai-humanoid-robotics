@echo off
echo Starting Physical AI & Humanoid Robotics RAG Chatbot System...
echo.

echo Checking environment variables...
if not defined COHERE_API_KEY (
    echo ❌ COHERE_API_KEY is not set
    echo Please set your Cohere API key in your environment or .env file
    pause
    exit /b 1
)

if not defined QDRANT_URL (
    echo ❌ QDRANT_URL is not set
    echo Please set your Qdrant URL in your environment or .env file
    pause
    exit /b 1
)

if not defined QDRANT_API_KEY (
    echo ❌ QDRANT_API_KEY is not set
    echo Please set your Qdrant API key in your environment or .env file
    pause
    exit /b 1
)

echo ✅ Environment variables are set
echo.

echo Starting backend server...
cd /d "D:\AI Book\physical-ai-humanoid-robotics"
start "RAG Chatbot Backend" cmd /k "cd backend && python run_server.py"

echo.
echo The backend server is now running on http://localhost:8000
echo.

echo To ingest content, run:
echo   cd backend && python content_ingestion.py
echo.

echo To test the system, run:
echo   python test_rag_system.py
echo.

echo Press any key to exit...
pause >nul