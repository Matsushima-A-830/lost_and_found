import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 非同期エンジン作成
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    future=True,
)

# セッションファクトリ
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# セッション依存性
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
