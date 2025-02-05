from pydantic import BaseSettings, Field
from datetime import timedelta

class BaseConfig(BaseSettings):
    """✅ Shared settings for both environments"""
    FLASK_ENV: str = "development"  # Still keeping the naming from Flask
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION: list = ["cookies"]
    JWT_COOKIE_SECURE: bool = True
    JWT_COOKIE_SAMESITE: str = "lax"
    JWT_COOKIE_HTTPONLY: bool = True
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=2)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=42)
    GOOGLE_CLIENT_ID: str = Field(..., env="GOOGLE_CLIENT")
    GOOGLE_SECRET: str = Field(..., env="GOOGLE_SECRET")

    class Config:
        env_file = ".env"

class DevelopmentConfig(BaseConfig):
    """✅ Development settings"""
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="SQLALCHEMY_DATABASE_URI")
    MONGO_URI: str = Field(..., env="MONGO_URI")
    JWT_COOKIE_SECURE: bool = False  # Allow HTTP in development
    JWT_COOKIE_CSRF_PROTECT: bool = False

class ProductionConfig(BaseConfig):
    """✅ Production settings"""
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="SQLALCHEMY_DATABASE_URI")
    MONGO_URI: str = Field(..., env="MONGO_URI")
    JWT_COOKIE_SECURE: bool = True  # Enforce HTTPS
    JWT_COOKIE_CSRF_PROTECT: bool = True  # Enable CSRF protection

import os
FLASK_ENV = os.getenv("FLASK_ENV", "development")
settings = DevelopmentConfig() if FLASK_ENV == "development" else ProductionConfig()
