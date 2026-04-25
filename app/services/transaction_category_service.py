import uuid

from sqlalchemy import Uuid
from sqlalchemy.orm import Session
from app.repositories.transaction_category_repo import TransactionCategoryRepo
from app.schemas.transaction_category import TransactionCategoryOut, TransactionCategoryCreate


class TransactionCategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TransactionCategoryRepo(db)

    async def get_all(self, parent: uuid) -> list[TransactionCategoryOut]:
        categories = await self.repo.get_all(parent=parent)
        return [TransactionCategoryOut.model_validate(c) for c in categories]

    async def create(self, category_in: TransactionCategoryCreate, parent: uuid = None) -> TransactionCategoryOut:
        category = await self.repo.create(name=category_in.name, description=category_in.description, parent=parent)
        return TransactionCategoryOut.model_validate(category)
