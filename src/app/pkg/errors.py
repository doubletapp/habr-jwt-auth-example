from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.pkg.exceptions import JsonHTTPException


class ErrorObj(BaseModel):
    type: str
    message: str


def json_http_exception_handler(request: Request, exc: JsonHTTPException) -> JSONResponse:
    return JSONResponse(
        content=exc.content,
        status_code=exc.status_code,
    )


def get_error_response(error: ErrorObj, status: int) -> JSONResponse:
    return JSONResponse(
        content={
            'type': error.type,
            'message': error.message,
        },
        status_code=status,
    )


def get_bad_request_error_response(error: ErrorObj) -> JSONResponse:
    return get_error_response(error, status=400)
