from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

# 標準化エラーレスポンス
def error_response(message: str, status_code: int = 400, data=None):
    return JSONResponse(
        status_code=status_code,
        content={"message": message, "data": data},
    )

# FastAPI例外ハンドラ
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(str(exc.detail), status_code=exc.status_code)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response("バリデーションエラー", status_code=422, data=exc.errors())

async def server_error_handler(request: Request, exc: Exception):
    return error_response("サーバーエラー", status_code=HTTP_500_INTERNAL_SERVER_ERROR)
