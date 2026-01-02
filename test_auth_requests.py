import requests
import json

# Test credentials
BASE_URL = "http://127.0.0.1:8080"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

def test_auth_flow():
    """Test the complete authentication flow using requests"""
    print("Testing registration...")
    register_response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
            "name": TEST_NAME
        }
    )
    print(f"Registration status: {register_response.status_code}")
    if register_response.status_code == 200:
        register_data = register_response.json()
        print(f"Registration successful: {register_data['email']}")
    else:
        print(f"Registration failed: {register_response.text}")
        return False

    print("\nTesting login...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        if "access_token" in login_data:
            token = login_data["access_token"]
            print("Login successful")
        else:
            print("Login failed - no token returned")
            return False
    else:
        print(f"Login failed: {login_response.text}")
        return False

    print("\nTesting user profile access...")
    profile_response = requests.get(
        f"{BASE_URL}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Profile access status: {profile_response.status_code}")
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"Profile access successful: {profile_data['name']}")
    else:
        print(f"Profile access failed: {profile_response.text}")
        return False

    print("\nTesting profile update...")
    update_response = requests.put(
        f"{BASE_URL}/api/auth/me",
        json={"name": "Updated Test User"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Profile update status: {update_response.status_code}")
    if update_response.status_code == 200:
        updated_data = update_response.json()
        print(f"Profile updated successfully: {updated_data['name']}")
    else:
        print(f"Profile update failed: {update_response.text}")
        return False

    print("\nAll authentication tests passed!")
    return True

if __name__ == "__main__":
    test_auth_flow()