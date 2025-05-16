from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_restx import Api
from config import config
from src.models import User, Post, Comment

# Initialize Flask extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api = Api(
    title="Social Media API",
    version="1.0",
    description="A simple social media API built with Flask, SQLAlchemy and Marshmallow",
    doc="/docs",
    security="Bearer Auth"
)


def create_app(config_name='default'):
    """
    Create a Flask application instance.

    :param config_name: The name of the configuration to use (default is 'default').
    :return: A Flask application instance.
    """
    app = Flask(__name__)

    # Load the configuration from the specified config name
    app.config.from_object(config[config_name])

    # Initialize extensions with the app context
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # JWT configuration
    from src.models import TokenBlacklist

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        """
        Check if the token is in the blacklist.

        :param jwt_header: The JWT header.
        :param jwt_payload: The JWT payload.

        :return: True if the token is in the blacklist, False otherwise.
        """
        jti = jwt_payload['jti']
        return TokenBlacklist.is_jti_blacklisted(jti)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        Callback for expired tokens.

        :param jwt_header: The JWT header.
        :param jwt_payload: The JWT payload.

        :return: A JSON response indicating the token has expired.
        """
        return {
            'status': 'fail',
            'message': 'Token has expired. Please log in again.'
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """
        Callback for invalid tokens.

        :param error: The error message.

        :return: A JSON response indicating the token is invalid.
        """
        return {
            'status': 'fail',
            'message': 'Invalid token. Please log in again.'
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """
        Callback for missing tokens.

        :param error: The error message.

        :return: A JSON response indicating the token is missing.
        """
        return {
            'status': 'fail',
            'message': 'Missing access token. Please log in.'
        }, 401

    # Register blueprints here if needed
    from apis import register_namespaces
    register_namespaces(api)

    @app.shell_context_processor
    def make_shell_context():
        """
        Create a shell context for the Flask application.

        :return: A dictionary containing the database and models.
        """
        return {
            'db': db,
            'User': User,
            'Post': Post,
            'Comment': Comment,
            'TokenBlacklist': TokenBlacklist,
        }

    return app
