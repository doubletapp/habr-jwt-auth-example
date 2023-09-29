import uuid
from datetime import timedelta

from app.pkg.auth.middlewares.jwt.base.config import JWTConfig


def generate_secret() -> str:
    return str(uuid.uuid4().hex)


def generate_plug_config(
    secret=generate_secret(),
    algorithm='HS256',
    access_token_ttl=timedelta(seconds=25),
    refresh_token_ttl=timedelta(seconds=50),
) -> JWTConfig:
    return JWTConfig(
        secret=secret,
        algorithm=algorithm,
        access_token_ttl=access_token_ttl,
        refresh_token_ttl=refresh_token_ttl,
    )
