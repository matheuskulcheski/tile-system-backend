import os
from datetime import timedelta

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key_change_in_production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tile_system_dev.db')

class TestingConfig(Config):
    """Configuração de teste"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tile_system_test.db'

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///tile_system_prod.db')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

