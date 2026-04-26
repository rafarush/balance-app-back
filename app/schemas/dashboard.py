from decimal import Decimal

from pydantic import BaseModel

from app.schemas.transaction import TransactionOut


class DashboardOut(BaseModel):
    balance: Decimal
    total_incomes: Decimal
    total_outcomes: Decimal
    last_incomes: list[TransactionOut]
    last_outcomes: list[TransactionOut]