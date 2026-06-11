from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise import ExerciseRecord
from app.schemas.exercise import ExerciseCreate, ExerciseSummary


async def create_exercise(db: AsyncSession, user_id: int, data: ExerciseCreate) -> ExerciseRecord:
    recorded_at = datetime.now(timezone.utc)
    if data.recorded_at:
        recorded_at = datetime.fromisoformat(data.recorded_at)

    exercise = ExerciseRecord(
        user_id=user_id,
        exercise_type=data.exercise_type,
        duration_min=data.duration_min,
        calories=data.calories,
        notes=data.notes,
        recorded_at=recorded_at,
    )
    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)
    return exercise


async def get_exercise(db: AsyncSession, user_id: int, exercise_id: int) -> ExerciseRecord | None:
    result = await db.execute(
        select(ExerciseRecord).where(ExerciseRecord.id == exercise_id, ExerciseRecord.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def list_exercises(db: AsyncSession, user_id: int, target_date: date | None = None) -> list[ExerciseRecord]:
    stmt = select(ExerciseRecord).where(ExerciseRecord.user_id == user_id)
    if target_date:
        start = datetime.combine(target_date, datetime.min.time())
        end = datetime.combine(target_date, datetime.max.time())
        stmt = stmt.where(ExerciseRecord.recorded_at.between(start, end))
    stmt = stmt.order_by(ExerciseRecord.recorded_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_exercise(db: AsyncSession, user_id: int, exercise_id: int, data: dict) -> ExerciseRecord | None:
    exercise = await get_exercise(db, user_id, exercise_id)
    if not exercise:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(exercise, key, value)

    await db.commit()
    await db.refresh(exercise)
    return exercise


async def delete_exercise(db: AsyncSession, user_id: int, exercise_id: int) -> bool:
    exercise = await get_exercise(db, user_id, exercise_id)
    if not exercise:
        return False
    await db.delete(exercise)
    await db.commit()
    return True


async def get_exercise_summary(db: AsyncSession, user_id: int, target_date: date | None = None) -> ExerciseSummary:
    exercises = await list_exercises(db, user_id, target_date)

    total_minutes = sum(e.duration_min for e in exercises)
    total_sessions = len(exercises)
    types = list(set(e.exercise_type for e in exercises))

    return ExerciseSummary(
        total_minutes=total_minutes,
        total_sessions=total_sessions,
        types=types,
    )
