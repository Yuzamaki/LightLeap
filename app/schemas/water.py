from pydantic import BaseModel


class WaterAdd(BaseModel):
    cups: int = 1  # 每次+1杯(200ml)


class WaterToday(BaseModel):
    cups: int = 0
    target_cups: int = 8
    progress_pct: float = 0.0
