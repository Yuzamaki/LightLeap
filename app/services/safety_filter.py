"""
安全过滤层：检测用户输入和 AI 输出中的不安全内容
"""

# 高危关键词 — 触发拦截
BLOCK_KEYWORDS = [
    "催吐", "泻药", "减肥药", "代餐", "断食", "绝食",
    "自残", "自杀", "割腕",
]

# 警告关键词 — 触发提醒但不拦截
WARN_KEYWORDS = [
    "节食", "不吃主食", "不吃晚饭", "断碳水",
    "胖", "肥", "好胖", "太胖",
]

# 输出中禁止的词汇
OUTPUT_BLOCK_PATTERNS = [
    "减肥药", "代餐推荐", "节食建议", "每顿只吃",
    "每天摄入低于", "卡路里严格限制",
]


def check_input_safety(message: str) -> tuple[bool, str | None]:
    """
    检查用户输入是否安全。
    返回 (is_safe, flag_reason)
    """
    msg_lower = message.lower()

    # 高危拦截
    for keyword in BLOCK_KEYWORDS:
        if keyword in msg_lower or keyword in message:
            return False, f"blocked_keyword:{keyword}"

    # 警告检测（不拦截，但标记）
    for keyword in WARN_KEYWORDS:
        if keyword in msg_lower or keyword in message:
            return True, f"warn_keyword:{keyword}"

    return True, None


def check_output_safety(reply: str) -> tuple[bool, str | None]:
    """
    检查 AI 输出是否包含不安全内容。
    返回 (is_safe, flag_reason)
    """
    for pattern in OUTPUT_BLOCK_PATTERNS:
        if pattern in reply:
            return False, f"blocked_pattern:{pattern}"

    return True, None


def get_safe_fallback() -> str:
    """安全检查不通过时的兜底回复"""
    return (
        "这个问题我暂时不太适合回答。健康最重要，如果你有什么担心，"
        "可以和爸爸妈妈或者信任的老师聊一聊。我也可以帮你联系专业的营养师～"
    )
