from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.auth.role import Role
from app.repositories.user_repo import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserOut


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> UserOut:
        existing = await self.repo.get_by_email(user_data.email)
        if existing:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed = hash_password(user_data.password)
        role = self.db.execute(select(Role).where(Role.name == "User")).scalar_one_or_none()
        user = await self.repo.create_user(email=user_data.email, hashed_password=hashed, name=user_data.name,
                                           surname=user_data.surname, role=role)
        return UserOut.model_validate(user)

    async def login(self, email: str, password: str) -> Token:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": str(user.id), "role": user.role.name})
        return Token(access_token=access_token)
