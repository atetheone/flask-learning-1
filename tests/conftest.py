"""
This module contains pytest fixtures for social media API tests.
"""

import pytest
import json
from src import create_app, db
from src.models import User, Post, Comment


@pytest.fixture(scope="module")
def app():
    """
    Create a Flask application instance for testing.
    """
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """
    Create a test client for the Flask application.

    Args:
        app: The Flask application instance.

    Returns:
        FlaskClient: A test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture(scope="module")
def db_session(app):
    """
    Create a database session for testing.

    Args:
        app: The Flask application instance.

    Returns:
        SQLAlchemy.session: session for the database.
    """
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def user_data():
    """
    Fixture to provide user data for testing.

    Returns:
        dict: A dictionary containing user data.
    """
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test@password123",
        "bio": "This is a test user.",
        "profile_picture": "http://example.com/profile.jpg",
    }


@pytest.fixture(scope="function")
def test_user(db_session, user_data):
    """
    Fixture to create a test user in the database.

    Args:
        db_session: The database session.
        user_data: The user data.

    Returns:
        User: The created user object.
    """
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        bio=user_data["bio"],
        profile_picture=user_data["profile_picture"],
    )
    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """
    Get authentication headers for the test user
    This fixture registers a user, logs them in, and returns the authentication headers.

    Args:
        client: The test client.
        test_user: The test user.

    Returns:
        dict: A dictionary containing authentication headers.
    """
    client.post('/auth/register', json=json.dumps(user_data))

    response = client.post(
        '/auth/login',
        json=json.dumps({"email": test_user.email, "password": test_user.password}),
    )

    tokens = json.loads(response.data)

    return {
        'Authorization': f"Bearer {tokens['access_token']}",
    }


@pytest.fixture(scope="function")
def post_data():
    """
    Fixture to provide post data for testing.

    Returns:
        dict: A dictionary containing post data.
    """
    return {"content": "This is a test post.", "visibility": "public"}


@pytest.fixture(scope="function")
def test_post(db_session, test_user, post_data):
    """
    Fixture to create a test post in the database.

    Args:
        db_session: The database session.
        test_user: The test user.
        post_data: The post data.

    Returns:
        Post: The created post object.
    """
    post = Post(
        visibility=post_data["visibility"],
        content=post_data["content"],
        user_id=test_user.user_id,
    )
    db_session.add(post)
    db_session.commit()

    return post


@pytest.fixture(scope="function")
def comment_data():
    """
    Fixture to provide comment data for testing.

    Returns:
        dict: A dictionary containing comment data.
    """
    return {"content": "This is a test comment."}


@pytest.fixture(scope="function")
def test_comment(db_session, test_user, test_post, comment_data):
    """
    Fixture to create a test comment in the database.

    Args:
        db_session: The database session.
        test_user: The test user.
        test_post: The test post.
        comment_data: The comment data.

    Returns:
        Comment: The created comment object.
    """
    comment = Comment(
        content=comment_data["content"],
        post_id=test_post.post_id,
        user_id=test_user.user_id,
    )
    db_session.add(comment)
    db_session.commit()

    return comment
