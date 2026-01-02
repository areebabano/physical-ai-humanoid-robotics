import asyncio
import httpx
import pytest
from backend.src.main import app

# Test credentials
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

@pytest.mark.asyncio
async def test_auth_flow():
    """Test the complete authentication flow: register, login, get profile, logout"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test registration
        print("Testing registration...")
        register_response = await client.post(
            "/api/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "name": TEST_NAME
            }
        )
        assert register_response.status_code == 200
        register_data = register_response.json()
        print(f"Registration successful: {register_data['email']}")

        # Test login
        print("Testing login...")
        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        token = login_data["access_token"]
        print("Login successful")

        # Test getting user profile with token
        print("Testing user profile access...")
        profile_response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["email"] == TEST_EMAIL
        print(f"Profile access successful: {profile_data['name']}")

        # Test updating profile
        print("Testing profile update...")
        update_response = await client.put(
            "/api/auth/me",
            json={"name": "Updated Test User"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["name"] == "Updated Test User"
        print(f"Profile updated successfully: {updated_data['name']}")

        print("All authentication tests passed!")

if __name__ == "__main__":
    asyncio.run(test_auth_flow())