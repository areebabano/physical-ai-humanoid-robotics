@echo off
REM Test script for RAG Chatbot System
REM Runs all tests for the backend and validates the system components

echo 🧪 Running RAG Chatbot System Tests...

REM Check prerequisites
echo 🔍 Checking prerequisites...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10+
    exit /b 1
) else (
    echo ✅ Python is available
)

pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip
    exit /b 1
) else (
    echo ✅ pip is available
)

REM Change to backend directory
cd backend

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo 📦 Installing backend dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
) else (
    echo ⚠️  requirements.txt not found in backend directory
)

REM Run the integration tests
echo 🚀 Running integration tests...
python test_integration.py

if errorlevel 1 (
    echo ❌ Integration tests failed!
    exit /b 1
) else (
    echo ✅ Integration tests passed!
)

REM Run any additional unit tests if they exist
if exist test_unit.py (
    echo 🧪 Running unit tests...
    python test_unit.py

    if errorlevel 1 (
        echo ❌ Unit tests failed!
        exit /b 1
    ) else (
        echo ✅ Unit tests passed!
    )
) else (
    echo ⚠️  No unit tests found (test_unit.py)
)

REM Check environment variables
echo 🔒 Checking environment variables...
set required_vars=OPENAI_API_KEY QDRANT_URL QDRANT_API_KEY DATABASE_URL

set missing_vars=
for %%v in (%required_vars%) do (
    if "!%%v!"=="" (
        set "missing_vars=!missing_vars! %%v"
    )
)

if defined missing_vars (
    echo ⚠️  Missing environment variables:!missing_vars!
    echo Some environment variables are missing - tests may fail
) else (
    echo ✅ All required environment variables are set
)

REM Run a basic API health check if the server is running
echo 📡 Checking API health...
curl -f -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    curl -f -s http://127.0.0.1:8000/health >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  API health check failed - server may not be running
    ) else (
        echo ✅ API health check passed
    )
) else (
    echo ✅ API health check passed
)

echo.
echo ✅ All tests completed successfully!
echo.
echo 📋 Test Summary:
echo    - Integration tests: PASSED
if exist test_unit.py echo    - Unit tests: PASSED
echo.
echo 🎉 RAG Chatbot System is ready for deployment!

pause