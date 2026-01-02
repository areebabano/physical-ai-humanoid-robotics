@echo off
REM Complete Setup Script for Physical AI & Humanoid Robotics RAG Chatbot
REM This script sets up and runs the complete system with proper port separation
REM Project location: D:\AI Book\physical-ai-humanoid-robotics

echo.
echo ================================================
echo PHYSICAL AI & HUMANOID ROBOTICS - Complete Setup
echo ================================================
echo.

REM Change to project directory
cd /d "D:\AI Book\physical-ai-humanoid-robotics"
echo Current directory: %cd%
echo.

REM Check if Python is available
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ and add it to your system PATH.
    pause
    exit /b 1
) else (
    echo Python is available.
)
echo.

REM Check if Node.js is available
echo [2/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH.
    echo Please install Node.js (version 18+) and add it to your system PATH.
    pause
    exit /b 1
) else (
    echo Node.js is available.
)
echo.

REM Check if Docker is available
echo [3/6] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Docker is not installed or not in PATH.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    echo After installation, restart your computer and run this script again.
    pause
    exit /b 1
) else (
    echo Docker is available.
)
echo.

REM Check if Qdrant is running
echo [4/6] Checking Qdrant status...
docker ps --filter "name=qdrant-container" --format "table {{.Names}}\t{{.Status}}" 2>nul
if errorlevel 1 (
    echo Docker not running. Please start Docker Desktop.
    pause
    exit /b 1
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
    curl -s http://localhost:6333/health >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Qdrant may not be ready. Please wait before starting backend.
    ) else (
        echo Qdrant is accessible and ready.
    )
)
echo.

REM Check if .env file exists
echo [5/6] Checking environment configuration...
if not exist ".env" (
    echo .env file not found. Creating from example...
    if exist ".env.example" (
        copy .env.example .env
        echo Created .env file from example. Please update with your actual API keys.
    ) else (
        echo ERROR: Neither .env nor .env.example found.
        echo Please create a .env file with proper configuration.
        pause
        exit /b 1
    )
) else (
    echo .env file exists.
)
echo.

REM Start Backend Server (port 8000) in new window
echo [6/6] Starting Backend Server (port 8000)...
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
echo WebSocket endpoint: ws://localhost:8000/ws
echo.
echo To stop services: Close the respective command prompt windows
echo ================================================
echo.

echo Setup complete! Your RAG chatbot system is now running.
echo.
echo Troubleshooting:
echo - If ports are busy, close existing processes on those ports
echo - Check .env file for correct API keys and settings
echo - Ensure Docker Desktop is running before starting services
echo - Check backend logs for any initialization errors
echo.

pause