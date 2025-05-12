"""
This module initializes the routes for the application.
It imports the necessary blueprints from the routes package
and registers them with the Flask application.
"""

from src.routes.auth import auth_bp
from src.routes.users import users_bp
from src.routes.posts import posts_bp
from src.routes.comments import comments_bp


def register_blueprints(app):
    """
    Register all blueprints with the Flask application.

    :param app: The Flask application instance.
    """

    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(users_bp, url_prefix="/api/v1")
    app.register_blueprint(posts_bp, url_prefix="/api/v1")
    app.register_blueprint(comments_bp, url_prefix="/api/v1")
