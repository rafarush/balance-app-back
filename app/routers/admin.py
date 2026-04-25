from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required
from app.models.user.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(policy_required("read-user"))])
async def list_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    repo = UserRepository(db)
    users = await repo.get_all(skip=skip, limit=limit)
    return [UserOut.model_validate(u) for u in users]
