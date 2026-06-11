from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.weight import WeightCreate, WeightRecordResponse, WeightTrendResponse
from app.services import weight_service

router = APIRouter()


@router.post("", response_model=WeightRecordResponse, status_code=201)
async def create_weight(
    data: WeightCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await weight_service.create_weight(db, current_user.id, data)


@router.get("/trend", response_model=WeightTrendResponse)
async def get_weight_trend(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await weight_service.get_weight_trend(db, current_user.id, days)
