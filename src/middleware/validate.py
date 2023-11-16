from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handler(request, exc)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        error_message = {"msg": error["msg"]}
        error_messages.append(error_message)

    return JSONResponse(
        status_code=409,
        content={"status_code": 409, "message": error["loc"][1] + " " + error["msg"]},
    )
