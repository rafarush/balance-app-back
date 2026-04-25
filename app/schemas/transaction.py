import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.transaction.transaction import TransactionType
from app.schemas.transaction_category import TransactionCategoryOut
from app.schemas.user import UserOut


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user: UserOut
    type: TransactionType
    amount: Decimal
    transaction_category: TransactionCategoryOut
    description: str
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime


class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: TransactionType
    amount: Decimal
    category_id: uuid.UUID
    description: str
    occurred_at: datetime
