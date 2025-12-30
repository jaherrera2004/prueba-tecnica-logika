from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.exceptions import ValidationError, AuthenticationError, AuthorizationError, NotFoundError, InternalServerError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Para errores de validación, tomar el primer error
    error_detail = exc.errors()[0]['msg'] if exc.errors() else "Error de validación"
    return JSONResponse(
        status_code=422,
        content={
            "detail": error_detail,
            "time": datetime.now().isoformat(),
            "success": False
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "time": datetime.now().isoformat(),
            "success": False
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "time": datetime.now().isoformat(),
            "success": False
        }
    )