from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcryot"], deprecated="auto")

class UserBase(BaseModel):
    """ Fields shared accross multiple User Validations"""
    email: EmailStr

class UserCreate(UserBase):
    """ Schema for user creation (extends UserBase). """
    password: str

    def hash_password(self) -> str:
        """Hash the password before storing it in the database"""
        return pwd_context.hash(self.password)
    
class UserRead(UserBase):
    """ Schema for return the user values """
    id: int
    created_at: datetime

    model_config = {"from_attributes": True} # ORM compatibility