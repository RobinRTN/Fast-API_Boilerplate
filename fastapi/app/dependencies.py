from fastapi_jwt_auth import AuthJWT
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi_socketio import SocketManager
from authlib.integrations.starlette_client import OAuth
from settings import settings

# Async DB Setup
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# MongoDb Setup
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client.get_default_database()

# Websocket
socket_manager = SocketManager()

oauth = OAuth()

def init_db(app):
    """ Initialize database connection """
    app.state.db = SessionLocal()

def init_jwt(app):
    """ Initialize JWT authentication """
    @AuthJWT.load_config
    def get_config():
        return settings

def init_mongo(app):
    """ Initialize MongoDB """
    app.state.mongo = mongo_db

def init_socketio(app):
    """ Initialize SocketIO """
    socket_manager.attach(app)

def init_oauth(app):
    """ Initialize OAuth providers """
    oauth.init_app(app)

def get_google_oauth(app):
    """ ✅ Registers Google OAuth """
    return oauth.register(
        name="google",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_SECRET,
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        client_kwargs={"scope": "openid email profile"},
    )
