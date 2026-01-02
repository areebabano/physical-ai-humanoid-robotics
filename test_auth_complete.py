import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

def test_auth_flow():
    print("Testing Authentication Flow...\n")

    # Test 1: Registration
    print("1. Testing Registration...")
    try:
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "name": TEST_NAME
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"   Registration Status: {register_response.status_code}")
        if register_response.status_code == 200:
            register_data = register_response.json()
            print(f"   Registration Success: {register_data.get('email')}")
        else:
            print(f"   Registration Failed: {register_response.text}")
            # If user already exists, continue to login
            if "already exists" in register_response.text:
                print("   User already exists, proceeding to login...")
            else:
                return False
    except Exception as e:
        print(f"   Registration Error: {str(e)}")
        return False

    # Test 2: Login
    print("\n2. Testing Login...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"   Login Status: {login_response.status_code}")
        if login_response.status_code == 200:
            login_data = login_response.json()
            if "access_token" in login_data:
                token = login_data["access_token"]
                print("   Login Success: Token received")
            else:
                print("   Login Failed: No token in response")
                return False
        else:
            print(f"   Login Failed: {login_response.text}")
            return False
    except Exception as e:
        print(f"   Login Error: {str(e)}")
        return False

    # Test 3: Access Protected Route (Get Profile)
    print("\n3. Testing Protected Route Access...")
    try:
        profile_response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Profile Access Status: {profile_response.status_code}")
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f"   Profile Access Success: {profile_data.get('name')}")
        else:
            print(f"   Profile Access Failed: {profile_response.text}")
            return False
    except Exception as e:
        print(f"   Profile Access Error: {str(e)}")
        return False

    # Test 4: Update Profile
    print("\n4. Testing Profile Update...")
    try:
        update_response = requests.put(
            f"{BASE_URL}/api/auth/me",
            json={"name": "Updated Test User"},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print(f"   Profile Update Status: {update_response.status_code}")
        if update_response.status_code == 200:
            updated_data = update_response.json()
            print(f"   Profile Update Success: {updated_data.get('name')}")
        else:
            print(f"   Profile Update Failed: {update_response.text}")
            return False
    except Exception as e:
        print(f"   Profile Update Error: {str(e)}")
        return False

    print("\n✅ All authentication tests passed!")
    return True

def test_server_connection():
    print("Testing Server Connection...\n")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Server Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please make sure the backend server is running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Server connection error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Authentication System Test Suite")
    print("="*40)

    # First, test if server is running
    if not test_server_connection():
        print("\nPlease start the backend server before running this test.")
        print("Run: cd backend && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload")
        exit(1)

    print()

    # Then run authentication tests
    success = test_auth_flow()

    print("\n" + "="*40)
    if success:
        print("🎉 All tests completed successfully!")
        print("The authentication system is working properly.")
    else:
        print("❌ Some tests failed.")
        print("Please check the backend logs for more details.")