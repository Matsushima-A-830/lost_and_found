import os
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from asgi_lifespan import LifespanManager

os.environ["DATABASE_URL"] = "postgresql+asyncpg://app:app@localhost:5432/app"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def async_client():
    from app.main import app
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
