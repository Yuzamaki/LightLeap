from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.water import WaterAdd, WaterToday
from app.services import water_service

router = APIRouter()


@router.post("", response_model=WaterToday)
async def add_water(
    data: WaterAdd = WaterAdd(),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cups = await water_service.add_water(db, current_user.id, data.cups)
    return await water_service.get_water_today(db, current_user.id)


@router.get("/today", response_model=WaterToday)
async def get_water_today(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await water_service.get_water_today(db, current_user.id)
