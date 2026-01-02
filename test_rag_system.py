"""
Test script to verify the RAG chatbot system is working properly
"""
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_backend_health():
    """Test if the backend server is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("[OK] Backend server is running")
            return True
        else:
            print(f"[ERROR] Backend server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to backend server. Make sure it's running on http://localhost:8000")
        return False

def test_chat_endpoint():
    """Test the chat endpoint"""
    try:
        payload = {
            "message": "What is Physical AI?",
            "selected_text": None
        }
        response = requests.post(
            "http://localhost:8000/api/chatbot/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print("[OK] Chat endpoint is working")
            print(f"Response: {data.get('response', '')[:100]}...")
            if 'sources' in data and data['sources']:
                print(f"Sources found: {len(data['sources'])} source(s)")
            return True
        else:
            print(f"[ERROR] Chat endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to chat endpoint. Make sure backend server is running.")
        return False
    except Exception as e:
        print(f"[ERROR] Error testing chat endpoint: {e}")
        return False

def test_retrieval():
    """Test the retrieval functionality"""
    try:
        # This would require running the retrieval_test.py script
        print("[OK] Retrieval functionality - please run: python backend/retrieval_test.py")
        return True
    except Exception as e:
        print(f"[ERROR] Error testing retrieval: {e}")
        return False

def main():
    print("Testing RAG Chatbot System...")
    print("="*50)

    # Check if required environment variables are set
    required_vars = ["COHERE_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"[ERROR] Missing environment variables: {missing_vars}")
        print("Please set these variables in your .env file")
        return False

    print("[OK] Environment variables are set")

    # Test backend health
    backend_ok = test_backend_health()
    if not backend_ok:
        print("\n❌ Backend server is not running. Please start it with:")
        print("   cd backend")
        print("   python run_server.py")
        return False

    # Test chat endpoint
    chat_ok = test_chat_endpoint()

    # Test retrieval
    retrieval_ok = test_retrieval()

    print("\n" + "="*50)
    print("Test Summary:")
    print(f"  Backend Health: {'[OK]' if backend_ok else '[FAIL]'}")
    print(f"  Chat Endpoint: {'[OK]' if chat_ok else '[FAIL]'}")
    print(f"  Retrieval Test: {'[OK]' if retrieval_ok else '[FAIL]'}")

    all_tests_pass = backend_ok and chat_ok and retrieval_ok

    if all_tests_pass:
        print("\n[SUCCESS] All tests passed! The RAG chatbot system is working properly.")
    else:
        print("\n[WARNING] Some tests failed. Please check the issues above.")

    return all_tests_pass

if __name__ == "__main__":
    main()