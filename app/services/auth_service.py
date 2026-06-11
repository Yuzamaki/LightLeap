import hashlib
from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.schemas.user import UserProfile, UserRegister


def _hash_phone(phone: str) -> str:
    return hashlib.sha256(f"{phone}:salt".encode()).hexdigest()


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def register_user(db: AsyncSession, data: UserRegister) -> User:
    phone_hash = _hash_phone(data.phone)

    # 检查手机号是否已注册
    existing = await db.execute(select(User).where(User.phone_hash == phone_hash))
    if existing.scalar_one_or_none():
        raise ValueError("该手机号已注册")

    user = User(
        nickname=data.nickname,
        phone_hash=phone_hash,
        age_group=data.age_group,
        gender=data.gender,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        fitness_level=data.fitness_level,
        goal=data.goal,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, phone: str, verify_code: str) -> str | None:
    # MVP 阶段：验证码固定为 000000
    if verify_code != "000000":
        return None

    phone_hash = _hash_phone(phone)
    result = await db.execute(select(User).where(User.phone_hash == phone_hash))
    user = result.scalar_one_or_none()
    if not user:
        return None

    return create_token(user.id)


async def get_profile(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one()


async def update_profile(db: AsyncSession, user_id: int, data: dict) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()

    for key, value in data.items():
        if value is not None:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user
