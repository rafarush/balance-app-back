import uuid
from datetime import timezone, datetime
from typing import List, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.transaction.transaction import TransactionType
from app.repositories.transaction_category_repo import TransactionCategoryRepo
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionOut, PaginatedTransactions


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

    async def get_all_transactions(self,
                                   user_id: uuid.UUID | None = None,
                                   tx_type: TransactionType | None = None,
                                   from_date: datetime | None = None,
                                   to_date: datetime | None = None,
                                   page: int = 1,
                                   limit: int = 20, ) -> PaginatedTransactions:
        transactions, total = await self.repo.get_paginated(
            user_id=user_id,
            tx_type=tx_type,
            from_date=from_date,
            to_date=to_date,
            page=page,
            limit=limit
        )
        return PaginatedTransactions(
            items=[TransactionOut.model_validate(t) for t in transactions],
            total=total,
            page=page,
            limit=limit,
        )
