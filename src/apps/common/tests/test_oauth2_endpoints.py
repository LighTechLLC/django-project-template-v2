import base64

from django.contrib.auth import get_user_model
from django.test import TestCase
from oauth2_provider.models import Application

User = get_user_model()


class OAuth2EndpointsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )

        # Create an OAuth2 application
        self.application = Application.objects.create(
            name="Test App",
            user=self.user,
            client_type="confidential",
            authorization_grant_type="password",
            client_secret="",
        )

    def _create_basic_auth_header(self):
        """Helper method to create Basic auth header"""
        credentials = (
            f"{self.application.client_id}:{self.application.client_secret}"
        )
        return f"Basic {base64.b64encode(credentials.encode()).decode()}"

    def test_token_endpoint_password_grant_success(self):
        """Test successful token request with password grant type"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        request_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "testpass123",
            "scope": "read",
        }

        # Act
        response = self.client.post(
            "/api/auth/token",
            data=request_data,
            headers={"Authorization": auth_header},
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertIn("token_type", data)
        self.assertIn("expires_in", data)
        self.assertEqual(data["token_type"], "Bearer")
        self.assertIn("refresh_token", data)

    def test_token_endpoint_invalid_credentials(self):
        """Test token request with invalid credentials"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        request_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "wrongpassword",
            "scope": "read",
        }

        # Act
        response = self.client.post(
            "/api/auth/token",
            data=request_data,
            headers={"Authorization": auth_header},
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "invalid_grant")

    def test_token_endpoint_invalid_client(self):
        """Test token request with invalid client credentials"""
        # Arrange
        request_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "testpass123",
            "client_id": "invalid_client_id",
            "client_secret": "invalid_client_secret",
        }

        # Act
        response = self.client.post("/api/auth/token", data=request_data)

        # Assert
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "invalid_client")

    def test_token_endpoint_missing_grant_type(self):
        """Test token request without grant_type"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        request_data = {
            "username": "test@example.com",
            "password": "testpass123",
        }

        # Act
        response = self.client.post(
            "/api/auth/token",
            data=request_data,
            headers={"Authorization": auth_header},
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "unsupported_grant_type")

    def test_refresh_token_grant(self):
        """Test refresh token grant type"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        initial_token_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "testpass123",
            "scope": "read",
        }

        # Act - Get initial token
        token_response = self.client.post(
            "/api/auth/token",
            data=initial_token_data,
            headers={"Authorization": auth_header},
        )

        # Assert initial token response
        self.assertEqual(token_response.status_code, 200)
        token_data = token_response.json()
        refresh_token = token_data["refresh_token"]

        # Arrange refresh token request
        refresh_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "read",
        }

        # Act - Use refresh token to get new access token
        response = self.client.post(
            "/api/auth/token",
            data=refresh_data,
            headers={"Authorization": auth_header},
        )

        # Assert refresh token response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)
        # Should be a different access token
        self.assertNotEqual(data["access_token"], token_data["access_token"])

    def test_revoke_token(self):
        """Test token revocation"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        token_request_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "testpass123",
            "scope": "read",
        }

        # Act - Get initial token
        token_response = self.client.post(
            "/api/auth/token",
            data=token_request_data,
            headers={"Authorization": auth_header},
        )

        # Assert token was obtained
        self.assertEqual(token_response.status_code, 200)
        token = token_response.json()["access_token"]

        # Arrange revocation request
        revoke_data = {"token": token}

        # Act - Revoke the token
        response = self.client.post(
            "/api/auth/revoke",
            data=revoke_data,
            headers={"Authorization": auth_header},
        )

        # Assert revocation was successful
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)

    def test_revoke_refresh_token(self):
        """Test refresh token revocation"""
        # Arrange
        auth_header = self._create_basic_auth_header()
        initial_token_data = {
            "grant_type": "password",
            "username": "test@example.com",
            "password": "testpass123",
            "scope": "read",
        }

        # Act - Get initial token
        token_response = self.client.post(
            "/api/auth/token",
            data=initial_token_data,
            headers={"Authorization": auth_header},
        )

        # Assert token was obtained
        self.assertEqual(token_response.status_code, 200)
        refresh_token = token_response.json()["refresh_token"]

        # Arrange revocation request
        revoke_data = {
            "token": refresh_token,
            "token_type_hint": "refresh_token",
        }

        # Act - Revoke the refresh token
        response = self.client.post(
            "/api/auth/revoke",
            data=revoke_data,
            headers={"Authorization": auth_header},
        )

        # Assert revocation was successful
        self.assertEqual(response.status_code, 200)

        # Arrange attempt to use revoked token
        refresh_attempt_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        # Act - Try to use the revoked refresh token
        refresh_response = self.client.post(
            "/api/auth/token",
            data=refresh_attempt_data,
            headers={"Authorization": auth_header},
        )

        # Assert revoked token cannot be used
        self.assertEqual(refresh_response.status_code, 400)
