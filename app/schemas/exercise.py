from datetime import datetime

from pydantic import BaseModel, Field


class ExerciseCreate(BaseModel):
    exercise_type: str = Field(..., description="运动类型")
    duration_min: int = Field(..., gt=0, description="时长(分钟)")
    calories: int | None = None
    notes: str | None = None
    recorded_at: str | None = None


class ExerciseUpdate(BaseModel):
    exercise_type: str | None = None
    duration_min: int | None = None
    calories: int | None = None
    notes: str | None = None


class ExerciseResponse(BaseModel):
    id: int
    user_id: int
    exercise_type: str
    duration_min: int
    calories: int | None
    notes: str | None
    recorded_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseSummary(BaseModel):
    total_minutes: int = 0
    total_sessions: int = 0
    types: list[str] = []
