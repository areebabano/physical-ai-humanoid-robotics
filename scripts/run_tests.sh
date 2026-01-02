#!/bin/bash

# Test script for RAG Chatbot System
# Runs all tests for the backend and validates the system components

set -e  # Exit immediately if a command exits with a non-zero status

echo "🧪 Running RAG Chatbot System Tests..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    printf "${GREEN}[SUCCESS]${NC} $1\n"
}

print_warning() {
    printf "${YELLOW}[WARNING]${NC} $1\n"
}

print_error() {
    printf "${RED}[ERROR]${NC} $1\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

if ! command_exists pip; then
    print_error "pip is not installed. Please install pip"
    exit 1
fi

print_status "Prerequisites check passed"

# Change to backend directory
cd backend

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_warning "requirements.txt not found in backend directory"
fi

# Run the integration tests
echo "🚀 Running integration tests..."
python test_integration.py

if [ $? -eq 0 ]; then
    print_status "Integration tests passed!"
else
    print_error "Integration tests failed!"
    exit 1
fi

# Run any additional unit tests if they exist
if [ -f "test_unit.py" ]; then
    echo ".UnitTesting running unit tests..."
    python test_unit.py

    if [ $? -eq 0 ]; then
        print_status "Unit tests passed!"
    else
        print_error "Unit tests failed!"
        exit 1
    fi
else
    print_warning "No unit tests found (test_unit.py)"
fi

# Check environment variables
echo "🔒 Checking environment variables..."
required_vars=("OPENAI_API_KEY" "QDRANT_URL" "QDRANT_API_KEY" "DATABASE_URL")

missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo "⚠️  Missing environment variables: ${missing_vars[*]}"
    print_warning "Some environment variables are missing - tests may fail"
else
    print_status "All required environment variables are set"
fi

# Run a basic API health check if the server is running
echo "📡 Checking API health..."
if curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
    print_status "API health check passed"
elif curl -f -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
    print_status "API health check passed"
else
    print_warning "API health check failed - server may not be running"
fi

# Run Python linting/checks if available
if command_exists flake8; then
    echo "🧹 Running code quality checks..."
    flake8 src/ --max-line-length=120 --exclude=__pycache__,.git,.venv
    print_status "Code quality checks passed"
else
    print_warning "flake8 not found - skipping code quality checks"
fi

# Run Python type checking if available
if command_exists mypy; then
    echo "🏷️  Running type checks..."
    mypy src/ --package backend.src
    print_status "Type checks passed"
else
    print_warning "mypy not found - skipping type checks"
fi

echo ""
echo "✅ All tests completed successfully!"
echo ""
echo "📋 Test Summary:"
echo "   - Integration tests: PASSED"
if [ -f "test_unit.py" ]; then
    echo "   - Unit tests: PASSED"
fi
if command_exists flake8; then
    echo "   - Code quality: PASSED"
fi
if command_exists mypy; then
    echo "   - Type checking: PASSED"
fi
echo ""
echo "🎉 RAG Chatbot System is ready for deployment!"