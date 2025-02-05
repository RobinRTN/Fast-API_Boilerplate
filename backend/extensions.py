from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
import os
from dotenv import find_dotenv
from authlib.integrations.flask_client import OAuth

find_dotenv()

# FLASK_ENV = os.getenv("FLASK_ENV", "development")
db = SQLAlchemy()
jwt = JWTManager()
mongo = PyMongo()
oauth = OAuth()

# async_mode = "eventlet" if FLASK_ENV == "production" else None
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet", logger=True, engineio_logger=True)

def get_google_oauth(app):
    """ ✅ Registers Google OAuth only when this function is called, avoiding circular imports. """
    return oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT"],
        client_secret=app.config["GOOGLE_SECRET"],
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        client_kwargs={"scope": "openid email profile"},
    )