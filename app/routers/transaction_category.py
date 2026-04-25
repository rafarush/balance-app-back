from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required, get_current_user
from app.models.user.user import User
from app.repositories.transaction_category_repo import TransactionCategoryRepo
from app.schemas.transaction_category import TransactionCategoryOut, TransactionCategoryCreate
from app.services.transaction_category_service import TransactionCategoryService

router = APIRouter(prefix="/transaction-category", tags=["transaction-category"])


@router.get("/",
            response_model=list[TransactionCategoryOut],
            dependencies=[Depends(policy_required("read-transaction"))]
            )
async def get_transaction_categories(
        db: Annotated[Session, Depends(get_db)],
        current_user: User = Depends(get_current_user)
) -> list[TransactionCategoryOut]:
    service = TransactionCategoryService(db)
    return await service.get_all(parent=current_user.id)


@router.post("/",
             response_model=TransactionCategoryOut,
             dependencies=[Depends(policy_required("create-transaction"))]
             )
async def create_transaction_category(
        db: Annotated[Session, Depends(get_db)],
        category_in: TransactionCategoryCreate,
        current_user: User = Depends(get_current_user)
) -> TransactionCategoryOut:
    service = TransactionCategoryService(db)
    return await service.create(category_in, current_user.id)
