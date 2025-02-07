from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas import UserCreate, UserRead
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, user_data: UserCreate) -> UserRead:
    """ Create a new user with a hashed password"""
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(email= user_data.email, password_hash=hashed_password)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return UserRead.model_validate(db_user)

async def get_user_by_id(db: AsyncSession, user_id: int) -> UserRead | None:
    """ Get a user thanks to its user_id """
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return UserRead.model_validate(user) if user else None

async def get_user_by_email(db: AsyncSession, email: str) -> UserRead | None:
    """ Get a user thanks to its email """
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    return UserRead.model_validate(user) if user else None

async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserRead | None:
    """ Authenticate user thanks to its given email and password """
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user and pwd_context.verify(password, user.password_hash):
        return UserRead.model_validate(user)
    return None

async def delete_user(db: AsyncSession, email: str) -> bool:
    """ Delete a user thanks to its given email address """
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()

    if user:
        await db.delete(user)
        await db.commit()
        return True
    
    return False