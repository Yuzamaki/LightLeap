from datetime import datetime

from pydantic import BaseModel, Field


class WeightCreate(BaseModel):
    weight_kg: float = Field(..., gt=0)
    recorded_at: str | None = None


class WeightRecordResponse(BaseModel):
    id: int
    user_id: int
    weight_kg: float
    recorded_at: datetime

    class Config:
        from_attributes = True


class WeightTrendPoint(BaseModel):
    date: str
    weight_kg: float
    smoothed: float | None = None


class WeightTrendResponse(BaseModel):
    points: list[WeightTrendPoint]
    current_weight: float | None = None
    trend: str = "stable"  # up / down / stable
    change_kg: float = 0.0
