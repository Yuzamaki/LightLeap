from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None  # 不传则新建会话


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    safety_flagged: bool = False


class MealRecognizeResponse(BaseModel):
    status: str = "not_implemented"
    message: str = "食物拍照识别功能开发中"
