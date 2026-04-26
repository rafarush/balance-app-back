from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import policy_required, get_current_user
from app.models.user.user import User
from app.schemas.dashboard import DashboardOut
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/",
            response_model=DashboardOut,
            dependencies=[Depends(policy_required("read-transaction"))]
            )
async def get_dashboard(db: Annotated[Session,
Depends(get_db)],
                        current_user: User = Depends(get_current_user)) -> DashboardOut:
    service = DashboardService(db=db)
    return await service.get_dashboard(current_user.id)
