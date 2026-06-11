from datetime import date, datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meal import MealRecord
from app.schemas.meal import FoodItem, MealCreate, MealSummary
from app.utils.food_data import classify_light_color, search_foods


async def create_meal(db: AsyncSession, user_id: int, data: MealCreate) -> MealRecord:
    recorded_at = datetime.now(timezone.utc)
    if data.recorded_at:
        recorded_at = datetime.fromisoformat(data.recorded_at)

    meal = MealRecord(
        user_id=user_id,
        meal_type=data.meal_type,
        foods=[f.model_dump() for f in data.foods],
        notes=data.notes,
        recorded_at=recorded_at,
    )
    db.add(meal)
    await db.commit()
    await db.refresh(meal)
    return meal


async def get_meal(db: AsyncSession, user_id: int, meal_id: int) -> MealRecord | None:
    result = await db.execute(
        select(MealRecord).where(MealRecord.id == meal_id, MealRecord.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def list_meals(db: AsyncSession, user_id: int, meal_date: date | None = None) -> list[MealRecord]:
    stmt = select(MealRecord).where(MealRecord.user_id == user_id)
    if meal_date:
        start = datetime.combine(meal_date, datetime.min.time())
        end = datetime.combine(meal_date, datetime.max.time())
        stmt = stmt.where(MealRecord.recorded_at.between(start, end))
    stmt = stmt.order_by(MealRecord.recorded_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_meal(db: AsyncSession, user_id: int, meal_id: int, data: dict) -> MealRecord | None:
    meal = await get_meal(db, user_id, meal_id)
    if not meal:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(meal, key, value)

    await db.commit()
    await db.refresh(meal)
    return meal


async def delete_meal(db: AsyncSession, user_id: int, meal_id: int) -> bool:
    meal = await get_meal(db, user_id, meal_id)
    if not meal:
        return False
    await db.delete(meal)
    await db.commit()
    return True


async def search_food(query: str) -> list[dict]:
    return search_foods(query)


async def get_meal_summary(db: AsyncSession, user_id: int, target_date: date | None = None) -> MealSummary:
    if target_date is None:
        target_date = date.today()

    meals = await list_meals(db, user_id, target_date)

    green_count = 0
    yellow_count = 0
    red_count = 0

    for meal in meals:
        for food in meal.foods:
            color = food.get("light_color", classify_light_color(food.get("category", "")))
            if color == "green":
                green_count += 1
            elif color == "red":
                red_count += 1
            else:
                yellow_count += 1

    total = green_count + yellow_count + red_count
    green_pct = green_count / total * 100 if total > 0 else 0
    yellow_pct = yellow_count / total * 100 if total > 0 else 0
    red_pct = red_count / total * 100 if total > 0 else 0

    # 生成建议
    suggestion = _generate_suggestion(green_pct, red_pct)

    return MealSummary(
        total=total,
        green_count=green_count,
        yellow_count=yellow_count,
        red_count=red_count,
        green_pct=round(green_pct, 1),
        yellow_pct=round(yellow_pct, 1),
        red_pct=round(red_pct, 1),
        suggestion=suggestion,
    )


def _generate_suggestion(green_pct: float, red_pct: float) -> str:
    if green_pct >= 60 and red_pct <= 10:
        return "今天吃得很棒！营养搭配很均衡 🥬"
    elif red_pct >= 40:
        return "今天红灯食物有点多，下次可以试试替换成蔬菜或水果～"
    elif green_pct >= 40:
        return "还不错！再加一份绿叶蔬菜就更完美了"
    else:
        return "尽量让每餐都有一份蔬菜或水果哦 🌱"
