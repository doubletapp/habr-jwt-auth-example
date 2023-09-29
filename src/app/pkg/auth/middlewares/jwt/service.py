from fastapi import Request, Security
from fastapi.security.api_key import APIKeyHeader
from jwt import decode, InvalidTokenError
from app.internal.users.models import APIUser

from app.pkg.auth.middlewares.jwt.errors import AccessError
from app.pkg.auth.middlewares.jwt.base.token_types import TokenType
from app.pkg.auth.middlewares.jwt.utils import check_revoked
from app.pkg.exceptions import JsonHTTPException
from config.settings import jwt_config


def __try_to_get_clear_token(authorization_header: str) -> str:
    if authorization_header is None:
        raise JsonHTTPException(content=dict(AccessError.get_token_is_not_specified_error()), status_code=400)

    if 'Bearer ' not in authorization_header:
        raise JsonHTTPException(content=dict(AccessError.get_incorrect_auth_header_form_error()), status_code=400)

    return authorization_header.replace('Bearer ', '')


async def check_access_token(
    request: Request,
    authorization_header: str = Security(APIKeyHeader(name='Authorization', auto_error=False))
) -> str:
    clear_token = __try_to_get_clear_token(authorization_header=authorization_header)

    try:
        payload = decode(jwt=clear_token, key=jwt_config.secret, algorithms=['HS256', 'RS256'])
        if payload['type'] != TokenType.ACCESS.value:
            raise JsonHTTPException(content=dict(AccessError.get_incorrect_token_type_error()), status_code=403)
    except InvalidTokenError:
        raise JsonHTTPException(content=dict(AccessError.get_invalid_token_error()), status_code=403)

    if await check_revoked(payload['jti']):
        raise JsonHTTPException(content=dict(AccessError.get_token_revoked_error()), status_code=403)

    user = await APIUser.filter(id=payload['sub']).first()
    if not user:
        raise JsonHTTPException(content=dict(AccessError.get_token_owner_not_found()), status_code=403)

    request.state.user = user
    request.state.device_id = payload['device_id']

    return authorization_header
