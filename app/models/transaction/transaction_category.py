import uuid

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TransactionCategory(Base):
    __tablename__ = 'transaction_category'

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parent: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # user: Mapped["User"] = relationship("User", back_populates="transactions_category")
