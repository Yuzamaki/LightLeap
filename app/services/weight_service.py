import statistics
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.weight import WeightRecord
from app.schemas.weight import WeightCreate, WeightTrendPoint, WeightTrendResponse


async def create_weight(db: AsyncSession, user_id: int, data: WeightCreate) -> WeightRecord:
    recorded_at = datetime.now(timezone.utc)
    if data.recorded_at:
        recorded_at = datetime.fromisoformat(data.recorded_at)

    record = WeightRecord(
        user_id=user_id,
        weight_kg=data.weight_kg,
        recorded_at=recorded_at,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    # 更新用户当前体重
    from app.models.user import User
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    user.weight_kg = data.weight_kg
    await db.commit()

    return record


async def get_weight_trend(db: AsyncSession, user_id: int, days: int = 30) -> WeightTrendResponse:
    since = datetime.now(timezone.utc) - timedelta(days=days)

    result = await db.execute(
        select(WeightRecord)
        .where(WeightRecord.user_id == user_id, WeightRecord.recorded_at >= since)
        .order_by(WeightRecord.recorded_at.asc())
    )
    records = result.scalars().all()

    if not records:
        return WeightTrendResponse(points=[], current_weight=None, trend="stable", change_kg=0.0)

    # 按日期分组取平均
    daily: dict[date, list[float]] = {}
    for r in records:
        d = r.recorded_at.date()
        daily.setdefault(d, []).append(r.weight_kg)

    dates = sorted(daily.keys())
    raw_weights = [sum(daily[d]) / len(daily[d]) for d in dates]

    # 7日移动平均平滑 (中位数)
    smoothed = []
    for i in range(len(raw_weights)):
        left = max(0, i - 3)
        right = min(len(raw_weights), i + 4)
        window = raw_weights[left:right]
        smoothed.append(statistics.median(window))

    points = [
        WeightTrendPoint(date=d.isoformat(), weight_kg=round(raw_weights[i], 1), smoothed=round(smoothed[i], 1))
        for i, d in enumerate(dates)
    ]

    current_weight = raw_weights[-1]
    if len(smoothed) >= 2:
        change = smoothed[-1] - smoothed[0]
        if abs(change) < 0.3:
            trend = "stable"
        elif change < 0:
            trend = "down"
        else:
            trend = "up"
        change_kg = round(change, 1)
    else:
        trend = "stable"
        change_kg = 0.0

    return WeightTrendResponse(
        points=points,
        current_weight=round(current_weight, 1),
        trend=trend,
        change_kg=change_kg,
    )
