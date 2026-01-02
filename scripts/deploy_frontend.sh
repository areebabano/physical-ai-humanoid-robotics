#!/bin/bash

# Deployment script for RAG Chatbot Frontend (Docusaurus)
# Builds and deploys the Docusaurus site to GitHub Pages or other hosting

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Deploying RAG Chatbot Frontend (Docusaurus)..."

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
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm"
    exit 1
fi

print_status "Prerequisites check passed"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "Missing package.json. Please run this script from the project root."
    exit 1
fi

# Install dependencies
print_step "Installing dependencies..."
npm install
print_status "Dependencies installed"

# Build the Docusaurus site
print_step "Building Docusaurus site..."
npm run build

if [ $? -ne 0 ]; then
    print_error "Build failed! Cannot proceed with deployment."
    exit 1
fi

print_status "Build completed successfully"

# Check if the build directory exists
if [ ! -d "build" ]; then
    print_error "Build directory does not exist. Build may have failed."
    exit 1
fi

# Deploy based on environment variable or default to GitHub Pages
if [ "$DEPLOY_PLATFORM" = "github_pages" ]; then
    print_step "Deploying to GitHub Pages..."

    # Check if git is available
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed or not in PATH"
        exit 1
    fi

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository. GitHub Pages deployment requires git."
        exit 1
    fi

    # Deploy to GitHub Pages
    GIT_USER=$(git config user.name)
    GIT_EMAIL=$(git config user.email)

    if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
        print_error "Git user.name and/or user.email not configured"
        print_warning "Run: git config --global user.name 'Your Name'"
        print_warning "Run: git config --global user.email 'your-email@example.com'"
        exit 1
    fi

    # Use the Docusaurus deploy command
    if npm run deploy > /dev/null 2>&1; then
        print_status "Deployed to GitHub Pages successfully"
    else
        print_error "GitHub Pages deployment failed"
        exit 1
    fi

elif [ "$DEPLOY_PLATFORM" = "netlify" ]; then
    print_step "Deploying to Netlify..."

    if command -v netlify &> /dev/null; then
        netlify deploy --dir=build --prod
        print_status "Deployed to Netlify successfully"
    else
        print_warning "Netlify CLI not found. Please install Netlify CLI:"
        print_warning "npm install -g netlify-cli"
        print_warning "Then run: netlify deploy --dir=build --prod"
    fi

elif [ "$DEPLOY_PLATFORM" = "vercel" ]; then
    print_step "Deploying to Vercel..."

    if command -v vercel &> /dev/null; then
        vercel --prod --public
        print_status "Deployed to Vercel successfully"
    else
        print_warning "Vercel CLI not found. Please install Vercel CLI:"
        print_warning "npm install -g vercel"
        print_warning "Then run: vercel --prod --public"
    fi

elif [ "$DEPLOY_PLATFORM" = "custom" ]; then
    print_step "Preparing custom deployment..."

    # Copy build files to a deployment directory
    DEPLOY_DIR=${DEPLOY_DIR:-"../deployment_files"}
    mkdir -p "$DEPLOY_DIR"
    cp -r build/* "$DEPLOY_DIR/"

    print_status "Build files copied to: $DEPLOY_DIR"
    print_warning "Custom deployment requires manual upload of files in $DEPLOY_DIR to your hosting provider"

else
    print_warning "No specific platform specified. Available options: github_pages, netlify, vercel, custom"
    echo "You can set DEPLOY_PLATFORM environment variable to automate deployment."
    echo "Defaulting to preparing files for manual deployment..."

    # Prepare for manual deployment
    DEPLOY_DIR=${DEPLOY_DIR:-"../docusaurus_build_$(date +%Y%m%d_%H%M%S)"}
    mkdir -p "$DEPLOY_DIR"
    cp -r build/* "$DEPLOY_DIR/"

    print_status "Build files prepared in: $DEPLOY_DIR"
    print_warning "Please upload the contents of $DEPLOY_DIR to your web server"
fi

# Verify deployment by checking if build files exist
print_step "Verifying deployment files..."
BUILD_FILES=$(find build -type f | wc -l)
echo "Found $BUILD_FILES files in build directory"

if [ "$BUILD_FILES" -gt 0 ]; then
    print_status "Deployment files verified"
else
    print_error "No build files found - deployment may have failed"
    exit 1
fi

print_step "Frontend deployment preparation completed!"

echo ""
echo "📋 Frontend Deployment Summary:"
echo "   - Platform: ${DEPLOY_PLATFORM:-manual}"
echo "   - Build directory: $(pwd)/build/"
echo "   - Files count: $BUILD_FILES"
echo "   - Status: SUCCESS"
echo ""
echo "🔗 Your Docusaurus site is ready to be deployed!"
echo ""
echo "💡 Configuration notes:"
echo "   - Make sure BACKEND_URL in your docusaurus.config.js points to your deployed backend"
echo "   - For GitHub Pages, ensure your site URL is correctly configured"
echo "   - For custom domains, update your DNS settings accordingly"
echo ""
echo "🎉 RAG Chatbot Frontend is ready for deployment!"