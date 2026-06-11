from datetime import date, datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.water import WaterRecord
from app.schemas.water import WaterToday
from app.utils.constants import WATER_CUP_ML


async def add_water(db: AsyncSession, user_id: int, cups: int = 1) -> int:
    """添加喝水量，返回当前总杯数"""
    record = WaterRecord(
        user_id=user_id,
        cups=cups,
        recorded_at=datetime.now(timezone.utc),
    )
    db.add(record)
    await db.commit()

    # 返回今日总杯数
    return await _today_cups(db, user_id)


async def get_water_today(db: AsyncSession, user_id: int) -> WaterToday:
    cups = await _today_cups(db, user_id)

    # 计算目标杯数
    result = await db.execute(select(User.weight_kg).where(User.id == user_id))
    weight = result.scalar() or 50  # 默认50kg
    target_ml = weight * 30 + 500  # 基础 + 运动加成
    target_cups = max(8, round(target_ml / WATER_CUP_ML))

    progress_pct = round(cups / target_cups * 100, 1) if target_cups > 0 else 0

    return WaterToday(cups=cups, target_cups=target_cups, progress_pct=progress_pct)


async def _today_cups(db: AsyncSession, user_id: int) -> int:
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    result = await db.execute(
        select(func.coalesce(func.sum(WaterRecord.cups), 0)).where(
            WaterRecord.user_id == user_id,
            WaterRecord.recorded_at.between(start, end),
        )
    )
    return result.scalar() or 0
