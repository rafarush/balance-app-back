import uuid
from datetime import datetime
from decimal import Decimal

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
            category=category,
            description=description,
            occurred_at=occurred_at,
        )
        self.db.add(transaction)
        self.db.flush()
        self.db.refresh(transaction)
        self.db.commit()
        return transaction

