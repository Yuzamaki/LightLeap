"""
食物拍照识别 —— 占位模块
后续实现：OpenAI Vision API 或自训练 YOLO 模型
"""

from app.schemas.chat import MealRecognizeResponse


async def recognize_meal(image_bytes: bytes) -> MealRecognizeResponse:
    """占位：暂时不实现食物拍照识别"""
    return MealRecognizeResponse(
        status="not_implemented",
        message="食物拍照识别功能开发中",
    )
