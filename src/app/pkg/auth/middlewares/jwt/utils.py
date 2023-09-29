import uuid
from jwt.exceptions import InvalidTokenError

from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.models import IssuedJWTToken


def generate_device_id() -> str:
    return str(uuid.uuid4())


async def check_revoked(jti: str) -> bool:
    return await IssuedJWTToken.filter(jti=jti, revoked=True).exists()


def try_decode_token(jwt_auth: JWTAuth, token: str) -> tuple[dict, None] | tuple[None, InvalidTokenError]:
    try:
        payload = jwt_auth.verify_token(token)
        return payload, None
    except InvalidTokenError as error:
        return None, error
