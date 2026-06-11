from pydantic import BaseModel


class DashboardToday(BaseModel):
    # 饮食
    meals_count: int = 0
    green_pct: float = 0
    yellow_pct: float = 0
    red_pct: float = 0
    diet_suggestion: str = ""

    # 运动
    exercise_minutes: int = 0
    exercise_sessions: int = 0

    # 喝水
    water_cups: int = 0
    water_target_cups: int = 8
    water_progress_pct: float = 0

    # 体重
    current_weight: float | None = None
    weight_trend: str = "stable"

    # 连续打卡
    streak_days: int = 0
