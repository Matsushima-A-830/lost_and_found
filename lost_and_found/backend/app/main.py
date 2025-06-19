# FastAPI エントリポイント
from fastapi import FastAPI
from .routers import items, analyze, police_reports, alerts, auth
from .utils import error_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="拾得物管理システム API")

# CORS (Electron/ローカル用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(police_reports.router, prefix="/api/police-reports", tags=["police_reports"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])

# エラーハンドラ
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await error_response.http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return await error_response.validation_exception_handler(request, exc)

@app.exception_handler(Exception)
async def custom_server_error_handler(request: Request, exc: Exception):
    return await error_response.server_error_handler(request, exc)
