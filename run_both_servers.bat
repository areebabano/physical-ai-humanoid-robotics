@echo off
REM RAG Chatbot System - Run Both Servers with Port Management
REM This script starts both backend and frontend on separate ports to avoid conflicts
REM Project location: D:\AI Book\physical-ai-humanoid-robotics

echo.
echo ================================================
echo RAG Chatbot System - Running Both Servers
echo ================================================
echo.

REM Change to project directory
cd /d "D:\AI Book\physical-ai-humanoid-robotics"
echo Current directory: %cd%
echo.

REM Check if Qdrant is running
echo Checking Qdrant status...
docker ps --filter "name=qdrant-container" --format "table {{.Names}}\t{{.Status}}" 2>nul
if errorlevel 1 (
    echo Docker not available or not running. Please install and start Docker Desktop.
    echo Then run: docker run -p 6333:6333 qdrant/qdrant
    echo.
) else (
    docker ps -q --filter "name=qdrant-container" | findstr . >nul
    if errorlevel 1 (
        echo Qdrant container not found, starting new container...
        docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
        echo Waiting for Qdrant to start...
        timeout /t 5 /nobreak >nul
    ) else (
        echo Qdrant container is already running
    )

    REM Verify Qdrant is accessible
    echo Checking Qdrant accessibility...
    curl -s http://localhost:6333/health >nul
    if errorlevel 1 (
        echo WARNING: Qdrant may not be ready. Please wait before starting backend.
    ) else (
        echo Qdrant is accessible and ready.
    )
    echo.
)

REM Start Backend Server (port 8000) in new window
echo Starting Backend Server (port 8000)...
start "RAG Backend Server" cmd /k "cd /d \"D:\AI Book\physical-ai-humanoid-robotics\" && echo Starting RAG Backend Server on port 8000... && echo NOTE: Close this window to stop the backend server && python run_server.py"
echo Backend server window opened on port 8000
echo.

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 8 /nobreak >nul

REM Start Frontend Server (port 3000) in new window
echo Starting Frontend Server (port 3000)...
start "RAG Frontend Server" cmd /k "cd /d \"D:\AI Book\physical-ai-humanoid-robotics\" && echo Starting Docusaurus Frontend Server on port 3000... && echo NOTE: Close this window to stop the frontend server && npx docusaurus start --port 3000"
echo Frontend server window opened on port 3000
echo.

REM Display system status
echo ================================================
echo System Running - Access URLs:
echo.
echo   Qdrant Vector DB: http://localhost:6333
echo   Backend API:      http://localhost:8000
echo   Frontend:         http://localhost:3000
echo.
echo Backend window title: RAG Backend Server
echo Frontend window title: RAG Frontend Server
echo.
echo To stop services: Close the respective command prompt windows
echo ================================================
echo.

pause