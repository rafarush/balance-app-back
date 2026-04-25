import uuid
from datetime import datetime
from decimal import Decimal
from typing import Tuple

from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from app.models.transaction.transaction import Transaction, TransactionType
from app.models.transaction.transaction_category import TransactionCategory


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create(
            self,
            user_id: uuid.UUID,
            type: TransactionType,
            amount: Decimal,
            category: TransactionCategory,
            description: str | None,
            occurred_at: datetime,
    ) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            type=type,
            amount=amount,
            transaction_category=category,
            description=description,
            occurred_at=occurred_at,
        )
        self.db.add(transaction)
        self.db.flush()
        self.db.refresh(transaction)
        self.db.commit()
        return transaction

    async def get_paginated(
            self,
            user_id: uuid.UUID | None = None,
            tx_type: TransactionType | None = None,
            from_date: datetime | None = None,
            to_date: datetime | None = None,
            page: int = 1,
            limit: int = 20,
    ) -> Tuple[list[Transaction], int]:
        query = select(Transaction)

        filters = []
        if user_id is not None:
            filters.append(Transaction.user_id == user_id)
        if tx_type is not None:
            filters.append(Transaction.type == tx_type)
        if from_date is not None:
            filters.append(Transaction.occurred_at >= from_date)
        if to_date is not None:
            filters.append(Transaction.occurred_at <= to_date)

        if filters:
            query = query.where(and_(*filters))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = self.db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(Transaction.occurred_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)

        result = self.db.execute(query)
        transactions = result.scalars().all()

        return list(transactions), total

