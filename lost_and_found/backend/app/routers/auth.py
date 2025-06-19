from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from datetime import timedelta
from app.models import USERS
from app.db import get_session
from app.auth import verify_password, create_access_token, create_refresh_token
from app.schemas import ErrorResponse
from app.deps import get_current_user
import os

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ALGORITHM = "HS256"

@router.post("/login", responses={401: {"model": ErrorResponse}})
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    stmt = select(USERS).where(USERS.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="ユーザー名またはパスワードが違います")
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=15),
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {
        "message": "ログイン成功",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    }

@router.post("/refresh")
async def refresh_token(
    data: dict,
):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="リフレッシュトークンが必要です")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="リフレッシュトークンが無効です")
    except JWTError:
        raise HTTPException(status_code=401, detail="リフレッシュトークンが無効です")
    access_token = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=15),
    )
    return {
        "message": "リフレッシュ成功",
        "data": {"access_token": access_token, "token_type": "bearer"},
    }

@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "message": "ユーザー情報取得成功",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role,
            "created_at": current_user.created_at,
        },
    }
