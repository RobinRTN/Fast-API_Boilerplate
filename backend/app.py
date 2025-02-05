import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from routes import register_all_blueprints
from extensions import db, jwt, mongo, socketio, oauth
from flask_migrate import Migrate
import eventlet
import eventlet.wsgi
from datetime import timedelta
from flask_cors import CORS

load_dotenv()
FLASK_ENV = os.getenv("FLASK_ENV", "development")

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = True  # ✅ Automatically makes cookies secure
    JWT_COOKIE_SAMESITE = "Lax"  # ✅ Automatically applies SameSite=Lax
    JWT_COOKIE_HTTPONLY = True  # ✅ Prevents JS access
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=42)
    MONGO_URI = os.getenv("MONGO_URI")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_SECRET")

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    JWT_COOKIE_SECURE = False  # Allow cookies over HTTP in development
    JWT_COOKIE_CSRF_PROTECT = False  # Disable CSRF protection in development

class ProductionConfig(Config):
    """Production-specific configuration."""
    JWT_COOKIE_SECURE = True  # Enforce HTTPS in production
    JWT_COOKIE_CSRF_PROTECT = True  # Enable CSRF protection in production

app = Flask(__name__)

if FLASK_ENV == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "http://localhost:4430",
    "https://picks-sous.xyz"
]}})

db.init_app(app)
migrate = Migrate(app, db)
jwt.init_app(app)
mongo.init_app(app)
socketio.init_app(app)
oauth.init_app(app)

register_all_blueprints(app)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"msg": "Bad request my dear...", "error": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"msg": "Ressource not found"}), 404


@app.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    app.logger.error(f"Database error: {error}")
    return jsonify({"msg": "DB error occured"}), 500

@app.errorhandler(Exception)
def general_error(error):
    return jsonify({"msg": "Internal error occured", "error": str(error)}), 500

if __name__ == "__main__":
    if FLASK_ENV == "development":
        print("Launching the app in development mode")
        socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    else:
        print("Launching the app via the right command to ensure it is launched with gunicorn")
        