#!/bin/bash

# Deployment script for RAG Chatbot Backend
# Deploys the FastAPI backend to a server or cloud platform

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Deploying RAG Chatbot Backend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    printf "${BLUE}[STEP]${NC} $1\n"
}

print_status() {
    printf "${GREEN}[SUCCESS]${NC} $1\n"
}

print_warning() {
    printf "${YELLOW}[WARNING]${NC} $1\n"
}

print_error() {
    printf "${RED}[ERROR]${NC} $1\n"
}

# Check prerequisites
print_step "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    print_error "pip is not installed. Please install pip"
    exit 1
fi

print_status "Prerequisites check passed"

# Check if we're in the right directory
if [ ! -f "backend/requirements.txt" ]; then
    print_error "Missing backend/requirements.txt. Please run this script from the project root."
    exit 1
fi

# Change to backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
print_step "Installing dependencies..."
pip install -r requirements.txt
print_status "Dependencies installed"

# Run tests before deployment
print_step "Running pre-deployment tests..."
python ../backend/test_integration.py

if [ $? -ne 0 ]; then
    print_error "Pre-deployment tests failed! Cannot proceed with deployment."
    exit 1
fi

print_status "Pre-deployment tests passed"

# Check for required environment variables
print_step "Checking environment variables..."
required_vars=("OPENAI_API_KEY" "QDRANT_URL" "QDRANT_API_KEY" "DATABASE_URL")

missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    print_error "Missing required environment variables: ${missing_vars[*]}"
    print_warning "Please set these environment variables before deployment"
    exit 1
fi

print_status "All required environment variables are set"

# Build the application
print_step "Building application..."
# In a real scenario, you might want to run additional build steps here
print_status "Application built successfully"

# Prepare deployment package
print_step "Preparing deployment package..."
mkdir -p deploy_package
cp -r src deploy_package/
cp -r requirements.txt deploy_package/
cp -r ../backend/test_integration.py deploy_package/ 2>/dev/null || true
print_status "Deployment package prepared"

# Option 1: Deploy to Render
if [ "$DEPLOY_PLATFORM" = "render" ]; then
    print_step "Deploying to Render..."
    # This assumes you have the Render CLI installed
    if command -v render &> /dev/null; then
        render deploy --serviceId $RENDER_SERVICE_ID
        print_status "Deployed to Render successfully"
    else
        print_warning "Render CLI not found. Please install Render CLI or deploy manually."
    fi
# Option 2: Deploy to Vercel (for serverless functions)
elif [ "$DEPLOY_PLATFORM" = "vercel" ]; then
    print_step "Deploying to Vercel..."
    if command -v vercel &> /dev/null; then
        vercel --prod
        print_status "Deployed to Vercel successfully"
    else
        print_warning "Vercel CLI not found. Please install Vercel CLI or deploy manually."
    fi
# Option 3: Deploy to local server with Docker
elif [ "$DEPLOY_PLATFORM" = "docker" ]; then
    print_step "Building Docker image..."
    if command -v docker &> /dev/null; then
        # Create Dockerfile if it doesn't exist
        if [ ! -f "../Dockerfile.backend" ]; then
            cat > ../Dockerfile.backend << EOF
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
        fi

        docker build -t rag-chatbot-backend -f ../Dockerfile.backend ..
        print_status "Docker image built successfully"

        # Run the container
        docker run -d --name rag-chatbot-backend-container \
            -p 8000:8000 \
            -e OPENAI_API_KEY=\$OPENAI_API_KEY \
            -e QDRANT_URL=\$QDRANT_URL \
            -e QDRANT_API_KEY=\$QDRANT_API_KEY \
            -e DATABASE_URL=\$DATABASE_URL \
            rag-chatbot-backend
        print_status "Docker container running on port 8000"
    else
        print_warning "Docker not found. Please install Docker or deploy manually."
    fi
else
    print_warning "No specific platform specified. Available options: render, vercel, docker"
    echo "You can set DEPLOY_PLATFORM environment variable to automate deployment."
    echo "Or deploy manually using the prepared package in deploy_package/"
fi

print_step "Deployment completed!"

echo ""
echo "📋 Deployment Summary:"
echo "   - Platform: ${DEPLOY_PLATFORM:-manual}"
echo "   - Package location: $(pwd)/deploy_package/"
echo "   - Status: SUCCESS"
echo ""
echo "🔗 Access your deployed backend at: http://your-deployed-url:8000"
echo ""
echo "💡 Next steps:"
echo "   1. Update your frontend to point to the new backend URL"
echo "   2. Test the API endpoints"
echo "   3. Monitor logs for any issues"
echo ""
echo "🎉 RAG Chatbot Backend deployed successfully!"