from pydantic import Field
from datetime import timedelta
from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    """✅ Shared settings for both environments"""
    FLASK_ENV: str = "development"  # Still keeping the naming from Flask
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_TOKEN_LOCATION: list = ["cookies"]
    JWT_COOKIE_SECURE: bool = True
    JWT_COOKIE_SAMESITE: str = "lax"
    JWT_COOKIE_HTTPONLY: bool = True
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(days=2)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=42)
    GOOGLE_CLIENT_ID: str = "1007725109700-h9go6r2e7bosait1f8u01sru5kqt7rdn.apps.googleusercontent.com"
    GOOGLE_SECRET: str = "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"

class DevelopmentConfig(BaseConfig):
    """✅ Development settings"""
    SQLALCHEMY_DATABASE_URI: str = "postgresql://neondb_owner:npg_DIAXOZJ1qVK9@ep-summer-lab-a2h71qkl-pooler.eu-central-1.aws.neon.tech/neondb"
    MONGO_URI: str = "mongodb+srv://robinrettien:uZyJE7EfSKlWnVnd@vintedscraper.eqode.mongodb.net/vinted_scraper_db?ssl=true&tlsAllowInvalidCertificates=true"
    JWT_COOKIE_SECURE: bool = False  # Allow HTTP in development
    JWT_COOKIE_CSRF_PROTECT: bool = False

class ProductionConfig(BaseConfig):
    """✅ Production settings"""
    SQLALCHEMY_DATABASE_URI: str = "postgresql://neondb_owner:npg_DIAXOZJ1qVK9@ep-summer-lab-a2h71qkl-pooler.eu-central-1.aws.neon.tech/neondb"
    MONGO_URI: str = "mongodb+srv://robinrettien:uZyJE7EfSKlWnVnd@vintedscraper.eqode.mongodb.net/vinted_scraper_db?ssl=true&tlsAllowInvalidCertificates=true"
    JWT_COOKIE_SECURE: bool = True  # Enforce HTTPS
    JWT_COOKIE_CSRF_PROTECT: bool = True  # Enable CSRF protection

import os
FLASK_ENV = os.getenv("FLASK_ENV", "development")
settings = DevelopmentConfig() if FLASK_ENV == "development" else ProductionConfig()