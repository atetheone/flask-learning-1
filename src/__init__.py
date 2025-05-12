from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config import config
from routes import register_blueprints

# Initialize Flask extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


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

    # Register blueprints here if needed
    register_blueprints(app)

    return app
