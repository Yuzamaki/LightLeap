import pytest

from app.services.safety_filter import check_input_safety, check_output_safety, get_safe_fallback


class TestSafetyFilter:
    """安全过滤单元测试（不需要数据库）"""

    def test_block_keywords(self):
        unsafe, reason = check_input_safety("我想催吐减肥")
        assert unsafe is False
        assert reason is not None
        assert "催吐" in reason

    def test_warn_keywords(self):
        safe, reason = check_input_safety("我最近在节食")
        assert safe is True
        assert reason is not None
        assert "节食" in reason

    def test_normal_message(self):
        safe, reason = check_input_safety("今天跑步很舒服")
        assert safe is True
        assert reason is None

    def test_output_block(self):
        safe, reason = check_output_safety("建议你吃代餐推荐的产品")
        assert safe is False

    def test_output_safe(self):
        safe, reason = check_output_safety("多吃蔬菜水果对身体好")
        assert safe is True

    def test_fallback(self):
        fallback = get_safe_fallback()
        assert "健康" in fallback


@pytest.mark.asyncio
async def test_meal_recognize_placeholder(auth_headers, client):
    """测试拍照识别占位接口"""
    files = {"image": ("test.jpg", b"fake_image_bytes", "image/jpeg")}
    resp = await client.post("/api/v1/ai/meal-recognize", headers=auth_headers, files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "not_implemented"
