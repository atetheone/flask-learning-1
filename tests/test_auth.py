"""
This module contains tests for the authentication endpoints of the social media API.
"""

import json
import pytest
from src.models import User, TokenBlocklist


def test_register_user(client, user_data):
    """
    Test successful user registration.

    Args:
        client (FlaskClient): The test client for the Flask application.
        user_data (dict): The user data for registration.
    """

    # Define the user data for registration
    unique_user = user_data.copy()
    unique_user["username"] = "uniqueuser"
    unique_user["email"] = "unique@example.com"

    # Send a POST request to the registration endpoint
    response = client.post(
        "auth/register",
        json=json.dumps(unique_user)
    )

    data = json.loads(response.data)

    # Assert the response status code and message
    assert response.status_code == 201
    assert "access_token" in data
    assert "refresh_token" in data
    assert "user" in data
    assert data["user"]["username"] == unique_user["username"]
    assert data["user"]["email"] == unique_user["email"]
