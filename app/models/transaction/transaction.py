import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import UUID, ForeignKey, Enum, Numeric, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user.user import User
from app.models.transaction.transaction_category import TransactionCategory


class TransactionType(str, PyEnum):
    INCOME = "income"
    OUTCOME = "outcome"


class Transaction(Base):
    __tablename__ = "transactions"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("transaction_category.id"),
                                                   nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(tz=timezone.utc), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    transaction_category: Mapped["TransactionCategory"] = relationship("TransactionCategory", back_populates="transactions")

