from datetime import datetime

from pydantic import BaseModel, Field


class FoodItem(BaseModel):
    food_name: str
    light_color: str = "yellow"  # green / yellow / red
    category: str = ""
    servings: float = 1.0


class MealCreate(BaseModel):
    meal_type: str = Field("lunch", description="breakfast/lunch/dinner/snack")
    foods: list[FoodItem] = Field(..., min_length=1)
    notes: str | None = None
    recorded_at: str | None = None  # ISO格式时间字符串，默认当前时间


class MealUpdate(BaseModel):
    meal_type: str | None = None
    foods: list[FoodItem] | None = None
    notes: str | None = None


class MealResponse(BaseModel):
    id: int
    user_id: int
    meal_type: str
    foods: list[FoodItem]
    notes: str | None
    photo_url: str | None
    recorded_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class MealSummary(BaseModel):
    total: int
    green_count: int
    yellow_count: int
    red_count: int
    green_pct: float = 0
    yellow_pct: float = 0
    red_pct: float = 0
    suggestion: str = ""


class FoodSearchResult(BaseModel):
    name: str
    category: str
    sub_category: str
    light_color: str
