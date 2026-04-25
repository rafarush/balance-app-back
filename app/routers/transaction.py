from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required, get_current_user
from app.models.user.user import User
from app.schemas.transaction import TransactionOut, TransactionCreate
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
