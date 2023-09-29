from fastapi import APIRouter, FastAPI

from app.pkg.auth.transport.handlers import auth_router
from app.internal.users.transport.handlers import me_router
from app.pkg.errors import json_http_exception_handler
from app.pkg.exceptions import JsonHTTPException
from config.settings import init_db

api_router = APIRouter(prefix='/api')

api_router.include_router(me_router)
api_router.include_router(auth_router)

app = FastAPI(
    title='JWT_Auth',
    exception_handlers={
        JsonHTTPException: json_http_exception_handler,
    },
)

app.include_router(api_router)

init_db(app=app)
