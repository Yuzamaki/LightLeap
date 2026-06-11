from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise import ExerciseRecord
from app.models.meal import MealRecord
from app.models.water import WaterRecord
from app.schemas.dashboard import DashboardToday
from app.schemas.meal import MealSummary
from app.schemas.water import WaterToday
from app.services.meal_service import get_meal_summary
from app.services.water_service import get_water_today
from app.services.weight_service import get_weight_trend


async def get_dashboard_today(db: AsyncSession, user_id: int) -> DashboardToday:
    # 并行获取各类数据
    meal_summary: MealSummary = await get_meal_summary(db, user_id, date.today())
    water_today: WaterToday = await get_water_today(db, user_id)
    weight_trend = await get_weight_trend(db, user_id, days=30)
    exercise_summary = await _get_today_exercise_summary(db, user_id)

    # 计算连续打卡天数
    streak = await _calculate_streak(db, user_id)

    return DashboardToday(
        meals_count=meal_summary.total,
        green_pct=meal_summary.green_pct,
        yellow_pct=meal_summary.yellow_pct,
        red_pct=meal_summary.red_pct,
        diet_suggestion=meal_summary.suggestion,
        exercise_minutes=exercise_summary["total_minutes"],
        exercise_sessions=exercise_summary["total_sessions"],
        water_cups=water_today.cups,
        water_target_cups=water_today.target_cups,
        water_progress_pct=water_today.progress_pct,
        current_weight=weight_trend.current_weight,
        weight_trend=weight_trend.trend,
        streak_days=streak,
    )


async def _get_today_exercise_summary(db: AsyncSession, user_id: int) -> dict:
    from datetime import datetime

    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    result = await db.execute(
        select(ExerciseRecord).where(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.recorded_at.between(start, end),
        )
    )
    exercises = result.scalars().all()

    return {
        "total_minutes": sum(e.duration_min for e in exercises),
        "total_sessions": len(exercises),
    }


async def _calculate_streak(db: AsyncSession, user_id: int) -> int:
    """计算连续有记录天数（饮食或运动）"""
    from datetime import datetime, timedelta

    # 查询最近 60 天有记录的日期
    since = datetime.now() - timedelta(days=60)

    meal_result = await db.execute(
        select(func.date(MealRecord.recorded_at))
        .where(MealRecord.user_id == user_id, MealRecord.recorded_at >= since)
        .distinct()
    )
    ex_result = await db.execute(
        select(func.date(ExerciseRecord.recorded_at))
        .where(ExerciseRecord.user_id == user_id, ExerciseRecord.recorded_at >= since)
        .distinct()
    )

    active_dates = set()
    for row in meal_result.scalars().all():
        active_dates.add(row)
    for row in ex_result.scalars().all():
        active_dates.add(row)

    if not active_dates:
        return 0

    # 从今天往回数连续天数
    streak = 0
    d = date.today()
    while d in active_dates:
        streak += 1
        d -= timedelta(days=1)

    return streak
