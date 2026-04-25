from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required
from app.models.user.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserOut
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(policy_required("read-user"))])
async def list_users(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    service = AdminService(db)
    return await service.get_all_users(skip=skip, limit=limit)
