import uuid

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.chat import ChatHistory
from app.models.user import User
from app.services.safety_filter import check_input_safety, check_output_safety, get_safe_fallback

SYSTEM_PROMPT = """你是「轻跃 App」的健康助手，名为"跃跃"。
你的身份是比用户大几岁的学长/学姐，亲切但不随便，专业但不枯燥。

【用户画像】
年龄层：{age_group}岁的{gender_text}
运动习惯：{fitness_text}
目标：{goal}

【回答约束】
1. 回复简短有温度（2-4 句话为佳），语气自然，可以适度幽默
2. 绝不推荐：节食、断食、代餐、减肥药、催吐、过度运动
3. 绝不使用这些词汇："胖""肥""瘦身""好身材"——重点说"健康""活力""舒服"
4. 如果用户表露焦虑/自卑情绪，先共情再给建议
5. 发现饮食失调迹象（长期不吃主食、每天 <800kcal），回复必须包含：
   "这听起来有点少，可以和我聊聊为什么这么吃吗？"
6. 回答开头不要'你好'或'您好'——直接说
7. 适当使用 emoji，但不堆砌（1-2个即可）
8. 只回答和健康、饮食、运动、生活习惯相关的问题。如果用户聊无关话题，友好地引导回健康方向"""


def _build_system_prompt(user: User) -> str:
    age_labels = {1: "13岁以下", 2: "13-15岁", 3: "16-18岁", 4: "19岁以上"}
    gender_labels = {0: "未设置", 1: "男生", 2: "女生"}
    fitness_labels = {1: "几乎不运动", 2: "偶尔运动", 3: "经常运动", 4: "每天运动"}

    return SYSTEM_PROMPT.format(
        age_group=age_labels.get(user.age_group, "未知"),
        gender_text=gender_labels.get(user.gender, "未设置"),
        fitness_text=fitness_labels.get(user.fitness_level, "未知"),
        goal=user.goal,
    )


async def chat_with_coach(
    db: AsyncSession,
    user: User,
    message: str,
    session_id: str | None = None,
) -> tuple[str, str, bool]:
    """
    与 AI 教练对话。
    返回 (reply, session_id, safety_flagged)
    """
    # 1. 输入安全检查
    is_safe, flag_reason = check_input_safety(message)
    if not is_safe:
        safe_reply = (
            "我注意到你的消息里有一些让我担心的内容。健康是第一位的，"
            "如果你遇到困难，可以和信任的人聊一聊。需要我帮你联系专业帮助吗？"
        )
        await _save_chat(db, user.id, session_id or str(uuid.uuid4()), "user", message, True, flag_reason)
        await _save_chat(db, user.id, session_id or str(uuid.uuid4()), "assistant", safe_reply, True, "safety_blocked")
        return safe_reply, session_id or str(uuid.uuid4()), True

    # 2. 生成或使用已有 session_id
    if not session_id:
        session_id = str(uuid.uuid4())

    # 3. 构建对话上下文
    system_prompt = _build_system_prompt(user)
    history = await _recent_history(db, user.id, limit=10)

    messages = [{"role": "system", "content": system_prompt}]
    for h in history:
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": message})

    # 4. 调用 LLM
    try:
        client = AsyncOpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        reply = response.choices[0].message.content or ""
    except Exception as e:
        reply = f"哎呀，教练现在有点卡住了 😅 稍等一下再来找我吧～"
        await _save_chat(db, user.id, session_id, "user", message, False, flag_reason)
        await _save_chat(db, user.id, session_id, "assistant", reply, False, None)
        return reply, session_id, False

    # 5. 输出安全检查
    output_safe, output_flag = check_output_safety(reply)
    if not output_safe:
        reply = get_safe_fallback()
        output_flag = "output_blocked"

    # 6. 保存对话历史
    await _save_chat(db, user.id, session_id, "user", message, bool(flag_reason), flag_reason)
    await _save_chat(db, user.id, session_id, "assistant", reply, bool(output_flag), output_flag)

    return reply, session_id, bool(flag_reason or output_flag)


async def chat_stream(
    db: AsyncSession,
    user: User,
    message: str,
    session_id: str | None = None,
):
    """
    流式对话生成器，yield SSE 格式文本。
    """
    is_safe, flag_reason = check_input_safety(message)
    if not is_safe:
        safe_reply = (
            "我注意到你的消息里有一些让我担心的内容。健康是第一位的，"
            "如果你遇到困难，可以和信任的人聊一聊。"
        )
        yield f"data: {safe_reply}\n\n"
        yield "data: [DONE]\n\n"
        return

    if not session_id:
        session_id = str(uuid.uuid4())

    system_prompt = _build_system_prompt(user)
    history = await _recent_history(db, user.id, limit=10)

    messages = [{"role": "system", "content": system_prompt}]
    for h in history:
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": message})

    try:
        client = AsyncOpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
        stream = await client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            stream=True,
        )

        full_reply = ""
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_reply += delta
                yield f"data: {delta}\n\n"

        yield "data: [DONE]\n\n"

        # 保存历史
        await _save_chat(db, user.id, session_id, "user", message, False, flag_reason)
        await _save_chat(db, user.id, session_id, "assistant", full_reply, False, None)

    except Exception:
        yield f"data: 教练卡住了 😅 等下再来找我吧～\n\n"
        yield "data: [DONE]\n\n"


async def _recent_history(db: AsyncSession, user_id: int, limit: int = 10) -> list[ChatHistory]:
    result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
    )
    return list(reversed(result.scalars().all()))


async def _save_chat(
    db: AsyncSession,
    user_id: int,
    session_id: str,
    role: str,
    content: str,
    safety_flagged: bool = False,
    flag_reason: str | None = None,
):
    chat = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        role=role,
        content=content,
        safety_flagged=safety_flagged,
        flag_reason=flag_reason,
    )
    db.add(chat)
    await db.commit()
