import pytest


@pytest.mark.asyncio
async def test_create_meal(auth_headers, client):
    resp = await client.post("/api/v1/meals", headers=auth_headers, json={
        "meal_type": "lunch",
        "foods": [
            {"food_name": "番茄炒蛋", "light_color": "green", "category": "蔬菜", "servings": 1},
            {"food_name": "白米饭", "light_color": "yellow", "category": "精制主食", "servings": 1},
        ],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["meal_type"] == "lunch"
    assert len(data["foods"]) == 2


@pytest.mark.asyncio
async def test_list_meals(auth_headers, client):
    # 先创建一条
    await client.post("/api/v1/meals", headers=auth_headers, json={
        "meal_type": "dinner",
        "foods": [{"food_name": "苹果", "light_color": "green", "category": "水果", "servings": 1}],
    })
    resp = await client.get("/api/v1/meals", headers=auth_headers)
    assert resp.status_code == 200
    meals = resp.json()
    assert len(meals) >= 1


@pytest.mark.asyncio
async def test_search_food(auth_headers, client):
    resp = await client.get("/api/v1/meals/search?q=番茄", headers=auth_headers)
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) > 0
    assert results[0]["name"] == "番茄炒蛋"


@pytest.mark.asyncio
async def test_meal_summary(auth_headers, client):
    await client.post("/api/v1/meals", headers=auth_headers, json={
        "meal_type": "lunch",
        "foods": [
            {"food_name": "番茄炒蛋", "light_color": "green", "category": "蔬菜", "servings": 1},
            {"food_name": "白米饭", "light_color": "yellow", "category": "精制主食", "servings": 1},
            {"food_name": "炸鸡", "light_color": "red", "category": "油炸", "servings": 1},
        ],
    })
    resp = await client.get("/api/v1/meals/summary", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 3
    assert data["green_count"] >= 1
    assert data["yellow_count"] >= 1
    assert data["red_count"] >= 1
    assert "suggestion" in data


@pytest.mark.asyncio
async def test_delete_meal(auth_headers, client):
    resp = await client.post("/api/v1/meals", headers=auth_headers, json={
        "meal_type": "snack",
        "foods": [{"food_name": "香蕉", "light_color": "green", "category": "水果", "servings": 1}],
    })
    meal_id = resp.json()["id"]
    resp = await client.delete(f"/api/v1/meals/{meal_id}", headers=auth_headers)
    assert resp.status_code == 200
    # 确认已删除
    resp = await client.get(f"/api/v1/meals/{meal_id}", headers=auth_headers)
    assert resp.status_code == 404
