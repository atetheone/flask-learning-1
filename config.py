"""
Configuration file for the application.
This file contains constants and settings used throughout the application.
"""

import os
from datetime import timedelta


class Config:
    """
    Config class containing application settings and constants.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///social_api.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-product')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]


class DevelopmentConfig(Config):
    """
    Development configuration class.
    Inherits from Config and sets the environment to development.
    """

    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration class.
    Inherits from Config and sets the environment to testing.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing


class ProductionConfig(Config):
    """
    Production configuration class.
    Inherits from Config and sets the environment to production.
    """

    DEBUG = False


# Dictionary to map environment names to configuration classes
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
