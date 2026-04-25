import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction.transaction_category import TransactionCategory


class TransactionCategoryRepo:
    def __init__(self, db: Session):
        self.db = db

    async def create(self, name: str, description: str, parent: uuid = None) -> TransactionCategory:
        category = TransactionCategory(name=name, description=description)
        if parent: category.parent = parent

        self.db.add(category)
        self.db.flush()
        self.db.refresh(category)
        self.db.commit()
        return category

    async def get_all(self, parent: uuid = None) -> list[TransactionCategory]:

        query = select(TransactionCategory)
        if parent:
            query = query.where(TransactionCategory.parent == parent)

        query = query.order_by(TransactionCategory.name.asc())
        result = self.db.execute(query)
        return list(result.scalars().all())
