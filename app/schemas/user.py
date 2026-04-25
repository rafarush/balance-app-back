import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.auth.role import Role


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    surname: str
    email: str
    role: Role


class UserInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    surname: str
    hashed_password: str
    role: Role
    is_active: bool
    created_at: datetime