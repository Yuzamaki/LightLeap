import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def client():
    from app.database import Base, engine
    from app.main import app

    # Drop & recreate all tables for clean test state
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_headers(client):
    """注册用户并返回带 token 的 headers"""
    await client.post("/api/v1/auth/register", json={
        "phone": "13800138000",
        "nickname": "测试用户",
        "age_group": 3,
        "gender": 1,
        "height_cm": 170,
        "weight_kg": 65,
        "fitness_level": 2,
        "goal": "更健康",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "phone": "13800138000",
        "verify_code": "000000",
    })
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
