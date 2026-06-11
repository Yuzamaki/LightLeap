import pytest


@pytest.mark.asyncio
async def test_register(client):
    resp = await client.post("/api/v1/auth/register", json={
        "phone": "13800138001",
        "nickname": "小明",
        "age_group": 3,
        "gender": 1,
        "goal": "更健康",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_code(client):
    resp = await client.post("/api/v1/auth/login", json={
        "phone": "13800138000",
        "verify_code": "123456",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_success(client):
    # 先注册
    await client.post("/api/v1/auth/register", json={
        "phone": "13800138002",
        "nickname": "小红",
        "age_group": 3,
        "gender": 2,
        "goal": "减重",
    })
    resp = await client.post("/api/v1/auth/login", json={
        "phone": "13800138002",
        "verify_code": "000000",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_get_profile(auth_headers, client):
    resp = await client.get("/api/v1/auth/profile", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["nickname"] == "测试用户"
    assert data["goal"] == "更健康"


@pytest.mark.asyncio
async def test_update_profile(auth_headers, client):
    resp = await client.put("/api/v1/auth/profile", headers=auth_headers, json={
        "nickname": "新名字",
        "weight_kg": 66.0,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["nickname"] == "新名字"
    assert data["weight_kg"] == 66.0


@pytest.mark.asyncio
async def test_duplicate_register(client):
    await client.post("/api/v1/auth/register", json={
        "phone": "13800138003",
        "nickname": "用户A",
        "age_group": 3,
        "goal": "更健康",
    })
    resp = await client.post("/api/v1/auth/register", json={
        "phone": "13800138003",
        "nickname": "用户B",
        "age_group": 3,
        "goal": "更健康",
    })
    assert resp.status_code == 400
