from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(50), default="新用户")
    phone_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    age_group: Mapped[int] = mapped_column(SmallInteger, default=3)  # 1:<13 2:13-15 3:16-18 4:19+
    gender: Mapped[int] = mapped_column(SmallInteger, default=0)  # 0未设置 1男 2女
    height_cm: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(nullable=True)
    fitness_level: Mapped[int] = mapped_column(SmallInteger, default=1)  # 1-5 几乎不/偶尔/经常/每天
    goal: Mapped[str] = mapped_column(String(30), default="更健康")  # 减重/增肌/更健康/体育考试
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
