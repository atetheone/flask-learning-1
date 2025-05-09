"""
This module initializes the Flask application and its extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config

# from app.models import Author, Book, Publisher, Category

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name="default"):
    """
    Create and configure the Flask application.

    Args:
       config_name (str): The configuration name to use (default is "default")

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    from app.routes import register_routes

    # Import models here to avoid circular imports
    from app.models import Author, Book, Publisher, Category

    register_routes(app)

    # Shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            app=app,
            db=db,
            Author=Author,
            Book=Book,
            Publisher=Publisher,
            Category=Category,
        )

    return app
