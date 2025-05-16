"""
This module initializes the routes for the application.
It imports the necessary blueprints from the routes package
and registers them with the Flask application.
"""

from src.apis.auth import auth_ns
from src.apis.users import users_ns
from src.apis.posts import posts_ns
from src.apis.comments import comments_ns


def register_namespaces(api):
    """
    Register all blueprints with the Flask application.

    :param app: The Flask application instance.
    """

    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
    api.add_namespace(posts_ns)
    api.add_namespace(comments_ns)
