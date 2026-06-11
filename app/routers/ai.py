from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, MealRecognizeResponse
from app.services import ai_coach, food_vision

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reply, session_id, flagged = await ai_coach.chat_with_coach(
        db, current_user, data.message, data.session_id
    )
    return ChatResponse(reply=reply, session_id=session_id, safety_flagged=flagged)


@router.get("/chat/stream")
async def chat_stream(
    message: str,
    session_id: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return StreamingResponse(
        ai_coach.chat_stream(db, current_user, message, session_id),
        media_type="text/event-stream",
    )


@router.post("/meal-recognize", response_model=MealRecognizeResponse)
async def meal_recognize(
    image: UploadFile,
    current_user: User = Depends(get_current_user),
):
    """食物拍照识别 —— 占位接口，功能开发中"""
    image_bytes = await image.read()
    return await food_vision.recognize_meal(image_bytes)
