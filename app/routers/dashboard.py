from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardToday
from app.services import dashboard_service

router = APIRouter()


@router.get("/today", response_model=DashboardToday)
async def get_dashboard_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await dashboard_service.get_dashboard_today(db, current_user.id)
