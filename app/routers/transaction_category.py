from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required, get_current_user
from app.models.user.user import User
from app.repositories.transaction_category_repo import TransactionCategoryRepo
from app.schemas.transaction_category import TransactionCategoryOut, TransactionCategoryCreate

router = APIRouter(prefix="/transaction-category", tags=["transaction-category"])


@router.get("/",
            response_model=list[TransactionCategoryOut],
            dependencies=[Depends(policy_required("read-transaction"))]
            )
async def get_transaction_categories(
        db: Annotated[Session, Depends(get_db)],
        current_user: User = Depends(get_current_user)
) -> list[TransactionCategoryOut]:
    repo = TransactionCategoryRepo(db)
    categories = await repo.get_all(parent=current_user.id)
    return [TransactionCategoryOut.model_validate(c) for c in categories]


@router.post("/",
             response_model=TransactionCategoryOut,
             dependencies=[Depends(policy_required("create-transaction"))]
             )
async def create_transaction_category(
        db: Annotated[Session, Depends(get_db)],
        category_in: TransactionCategoryCreate,
        current_user: User = Depends(get_current_user)
) -> TransactionCategoryOut:
    repo = TransactionCategoryRepo(db)
    category = await repo.create(name=category_in.name, description=category_in.description, parent=current_user.id)
    return TransactionCategoryOut.model_validate(category)
