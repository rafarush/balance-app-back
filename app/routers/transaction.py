from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required, get_current_user
from app.models.transaction.transaction import TransactionType
from app.models.user.user import User
from app.schemas.transaction import TransactionOut, TransactionCreate, PaginatedTransactions
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/",
             response_model=TransactionOut,
             dependencies=[Depends(policy_required("create-transaction"))]
             )
async def create_transaction(
        db: Annotated[Session, Depends(get_db)],
        transaction_in: TransactionCreate,
        current_user: User = Depends(get_current_user)
) -> TransactionOut:
    service = TransactionService(db)
    return await service.create_transaction(transaction_in, current_user.id)


@router.get("/",
            response_model=PaginatedTransactions,
            dependencies=[Depends(policy_required("read-transaction"))]
            )
async def list_transactions(
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
    type: TransactionType | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
):
    service = TransactionService(db)
    return await service.get_all_transactions(
        user_id=current_user.id,
        tx_type=type,
        from_date=from_date,
        to_date=to_date,
        page=page,
        limit=limit,
    )


