from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseResponse,
    ExerciseSummary,
    ExerciseUpdate,
)
from app.services import exercise_service

router = APIRouter()


@router.post("", response_model=ExerciseResponse, status_code=201)
async def create_exercise(
    data: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await exercise_service.create_exercise(db, current_user.id, data)
    return exercise


@router.get("", response_model=list[ExerciseResponse])
async def list_exercises(
    date: str | None = Query(None, description="日期 YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    target_date = date_type.fromisoformat(date) if date else None
    exercises = await exercise_service.list_exercises(db, current_user.id, target_date)
    return exercises


@router.get("/summary", response_model=ExerciseSummary)
async def exercise_summary(
    date: str | None = Query(None, description="日期 YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    target_date = date_type.fromisoformat(date) if date else None
    return await exercise_service.get_exercise_summary(db, current_user.id, target_date)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await exercise_service.get_exercise(db, current_user.id, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="记录不存在")
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    data: ExerciseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await exercise_service.update_exercise(
        db, current_user.id, exercise_id, data.model_dump(exclude_none=True)
    )
    if not exercise:
        raise HTTPException(status_code=404, detail="记录不存在")
    return exercise


@router.delete("/{exercise_id}")
async def delete_exercise(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    deleted = await exercise_service.delete_exercise(db, current_user.id, exercise_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"message": "删除成功"}
