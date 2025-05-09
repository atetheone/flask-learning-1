"""
This module is responsible for registering all the route blueprints"""

from app.routes.authors import authors_bp
from app.routes.books import books_bp
from app.routes.categories import categories_bp
from app.routes.publishers import publishers_bp


def register_routes(app):
    """
    Registers all the route blueprints with the Flask application.

    Args:
        app: The Flask application instance to register blueprints with.
    """
    app.register_blueprint(authors_bp, url_prefix="/api/authors")
    app.register_blueprint(publishers_bp, url_prefix="/api/publishers")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(books_bp, url_prefix="/api/books")
