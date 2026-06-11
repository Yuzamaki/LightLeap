from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    verify_code: str = Field("000000", description="验证码，MVP默认000000")
    nickname: str = Field("新用户", max_length=50)
    age_group: int = Field(3, ge=1, le=4, description="1:<13 2:13-15 3:16-18 4:19+")
    gender: int = Field(0, ge=0, le=2, description="0未设置 1男 2女")
    height_cm: int | None = None
    weight_kg: float | None = None
    fitness_level: int = Field(1, ge=1, le=4)
    goal: str = "更健康"


class UserLogin(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)
    verify_code: str = Field("000000")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: int
    nickname: str
    age_group: int
    gender: int
    height_cm: int | None
    weight_kg: float | None
    fitness_level: int
    goal: str

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    nickname: str | None = None
    height_cm: int | None = None
    weight_kg: float | None = None
    fitness_level: int | None = None
    goal: str | None = None
