import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user.user import User
from app.models.auth.role import Role


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, email: str, hashed_password: str, name: str, surname: str, role: Role) -> User:
        user = User(email=email, hashed_password=hashed_password, name=name, surname=surname, role=role)
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        self.db.commit()
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        result = self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
