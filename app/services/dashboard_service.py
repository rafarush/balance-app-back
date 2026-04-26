import uuid

from sqlalchemy.orm import Session

from app.models.transaction.transaction import TransactionType
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.dashboard import DashboardOut
from app.schemas.transaction import PaginatedTransactions, BalanceOut, TransactionOut


class DashboardService:
    def __init__(self, db: Session):
        self.db = db
        self.trans_repo = TransactionRepository(db)

    async def get_dashboard(self, user_id: uuid.UUID | None = None) -> DashboardOut:
        balance, total_incomes, total_outcomes = await self.trans_repo.get_balance_summary(user_id)
        last_incomes = await self.trans_repo.get_last_n_by_type(user_id, TransactionType.INCOME, n=10)
        last_outcomes = await self.trans_repo.get_last_n_by_type(user_id, TransactionType.OUTCOME, n=10)

        return DashboardOut(
            balance=balance,
            total_incomes=total_incomes,
            total_outcomes=total_outcomes,
            last_incomes=[TransactionOut.model_validate(t) for t in last_incomes],
            last_outcomes=[TransactionOut.model_validate(t) for t in last_outcomes],
        )

    # async def get_last_n_transactions_by_type(self,
    #                                           tx_type: TransactionType,
    #                                           user_id: uuid.UUID | None = None,
    #                                           n: int = 10) -> PaginatedTransactions:
    #     transactions = await self.trans_repo.get_last_n_by_type(
    #         tx_type=tx_type,
    #         user_id=user_id,
    #         n=n,
    #     )
    #     return PaginatedTransactions(
    #         items=transactions,
    #         total=len(transactions),
    #         page=1,
    #         limit=n,
    #     )
    #
    # async def get_balance(self, user_id: uuid.UUID | None = None) -> BalanceOut:
    #     balance = await self.trans_repo.get_balance_summary(user_id=user_id)
    #     return BalanceOut.model_validate(balance)
