from environs import Env
from datetime import timedelta
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.pkg.auth.middlewares.jwt.base.config import JWTConfig


env = Env()
env.read_env()

API_SECRET = env('API_SECRET')
HASH_SALT = env('HASH_SALT')

JWT_SECRET = env('JWT_SECRET')
ACCESS_TOKEN_TTL = env.int('ACCESS_TOKEN_TTL')
REFRESH_TOKEN_TTL = env.int('REFRESH_TOKEN_TTL')
jwt_config = JWTConfig(
    secret=JWT_SECRET,
    access_token_ttl=timedelta(seconds=ACCESS_TOKEN_TTL),
    refresh_token_ttl=timedelta(seconds=REFRESH_TOKEN_TTL),
)

# DB settings
POSTGRES_USER = env('POSTGRES_USER')
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
POSTGRES_HOST = env('POSTGRES_HOST')
POSTGRES_DB = env('POSTGRES_DB')

TORTOISE_ORM = {
    'connections': {'default': f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'},
    'apps': {
        'models': {
            'models': ['app.internal.models'],
            'default_connection': 'default',
        },
    },
}

generate_schemas = True


def switch_to_test_mode() -> None:
    global TORTOISE_ORM, generate_schemas
    test_db_url = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/test_{POSTGRES_DB}'
    TORTOISE_ORM['connections']['default'] = test_db_url
    generate_schemas = True


def init_db(app: FastAPI) -> None:
    register_tortoise(app=app, config=TORTOISE_ORM, add_exception_handlers=True, generate_schemas=generate_schemas)
