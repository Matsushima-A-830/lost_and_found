# POST /api/items 正常系テスト
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_create_item(async_client: AsyncClient):
    payload = {
        "found_datetime": "2024-06-01T12:00:00",
        "found_place": "駅前",
        "category_l": "財布",
        "status": "保管中"
    }
    # テスト用ユーザー認証トークンをセット（admin:admin）
    # ここでは認証をバイパスするか、テスト用トークンを生成する必要あり
    # 例: テスト用にJWTを直接生成
    from app.auth import create_access_token
    token = create_access_token({"sub": "1"})
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.post("/api/items/", json=payload, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
