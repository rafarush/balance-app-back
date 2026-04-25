import uuid
from datetime import timezone, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.repositories.transaction_category_repo import TransactionCategoryRepo
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionOut


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TransactionRepository(db)
        self.transaction_category_repo = TransactionCategoryRepo(db)

    async def create_transaction(self, transaction_in: TransactionCreate, user_id: uuid.UUID) -> TransactionOut:
        category = await self.transaction_category_repo.get_by_id(transaction_in.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {transaction_in.category_id} does not exist"
            )
        now = datetime.now(tz=timezone.utc)
        transaction = await self.repo.create(user_id=user_id,
                                             category=category,
                                             type=transaction_in.type,
                                             amount=transaction_in.amount,
                                             description=transaction_in.description,
                                             occurred_at=now
                                             )

        return TransactionOut.model_validate(transaction)
