# config.py
"""
Application configuration module.
Supports different environments (development, production) via environment variables.
"""

import os


class Config:
    """Base configuration class with default settings."""
    
    # Security - Use environment variable or generate random (for dev only)
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'assets.db')
    
    # Application settings
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'assets.db')


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    
    # In production, SECRET_KEY must be set via environment variable
    @property
    def SECRET_KEY(self):
        secret = os.environ.get('SECRET_KEY')
        if not secret:
            raise ValueError("SECRET_KEY environment variable must be set in production!")
        return secret


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Get the appropriate configuration based on FLASK_ENV environment variable.
    Defaults to development if not set.
    """
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])()
