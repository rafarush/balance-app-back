from sqlalchemy.orm import Session

from app.repositories.user_repo import UserRepository
from app.schemas.user import UserOut


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserOut]:
        users = await self.repo.get_all(skip=skip, limit=limit)
        return [UserOut.model_validate(u) for u in users]
