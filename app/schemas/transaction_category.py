import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionCategoryCreate(BaseModel):
    name: str
    description: str


class TransactionCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str


class TransactionCategoryFlattenedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
