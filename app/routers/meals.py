from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.meal import (
    FoodSearchResult,
    MealCreate,
    MealResponse,
    MealSummary,
    MealUpdate,
)
from app.services import meal_service

router = APIRouter()


@router.post("", response_model=MealResponse, status_code=201)
async def create_meal(
    data: MealCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    meal = await meal_service.create_meal(db, current_user.id, data)
    return meal


@router.get("", response_model=list[MealResponse])
async def list_meals(
    date: str | None = Query(None, description="日期 YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    target_date = date_type.fromisoformat(date) if date else None
    meals = await meal_service.list_meals(db, current_user.id, target_date)
    return meals


@router.get("/search", response_model=list[FoodSearchResult])
async def search_food(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    current_user: User = Depends(get_current_user),
):
    results = await meal_service.search_food(q)
    return results


@router.get("/summary", response_model=MealSummary)
async def meal_summary(
    date: str | None = Query(None, description="日期 YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    target_date = date_type.fromisoformat(date) if date else date_type.today()
    return await meal_service.get_meal_summary(db, current_user.id, target_date)


@router.get("/{meal_id}", response_model=MealResponse)
async def get_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    meal = await meal_service.get_meal(db, current_user.id, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="记录不存在")
    return meal


@router.put("/{meal_id}", response_model=MealResponse)
async def update_meal(
    meal_id: int,
    data: MealUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    meal = await meal_service.update_meal(db, current_user.id, meal_id, data.model_dump(exclude_none=True))
    if not meal:
        raise HTTPException(status_code=404, detail="记录不存在")
    return meal


@router.delete("/{meal_id}")
async def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    deleted = await meal_service.delete_meal(db, current_user.id, meal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"message": "删除成功"}
