from app.internal.users.models import APIUser
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.middlewares.jwt.base.token_types import TokenType
from app.pkg.auth.middlewares.jwt.errors import AccessError
from app.pkg.auth.middlewares.jwt.utils import check_revoked, generate_device_id, try_decode_token
from app.pkg.auth.errors import AuthError
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.auth.dto import TokensDTO, UserCredentialsDTO
from app.pkg.errors import ErrorObj
from app.pkg.utils import get_sha256_hash


class AuthService:
    def __init__(self, jwt_auth: JWTAuth) -> None:
        self._jwt_auth = jwt_auth

    async def register(self, body: UserCredentialsDTO) -> tuple[TokensDTO, None] | tuple[None, ErrorObj]:
        if await APIUser.filter(email=body.email).exists():
            return None, AuthError.get_email_occupied_error()

        user = await APIUser.create(email=body.email, password_hash=get_sha256_hash(line=body.password))

        access_token, refresh_token = await self._issue_tokens_for_user(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token), None

    async def login(self, body: UserCredentialsDTO) -> tuple[TokensDTO, None] | tuple[None, ErrorObj]:
        user = await APIUser.filter(email=body.email, password_hash=get_sha256_hash(line=body.password)).first()
        
        if not user:
            return None, AuthError.get_invalid_credentials_error()

        access_token, refresh_token = await self._issue_tokens_for_user(user=user)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token), None

    async def logout(self, user: APIUser, device_id: str) -> None:
        await user.tokens.filter(device_id=device_id).update(revoked=True)

    async def update_tokens(self, user: APIUser, refresh_token: str) -> tuple[TokensDTO, None] | tuple[None, ErrorObj]:
        payload, error = try_decode_token(jwt_auth=self._jwt_auth, token=refresh_token)

        if error:
            return None, AccessError.get_invalid_token_error()

        if payload['type'] != TokenType.REFRESH.value:
            return None, AccessError.get_incorrect_token_type_error()

        user = await APIUser.filter(id=payload['sub']).first()

        # Если обновленный токен пробуют обновить ещё раз,
        # нужно отменить все выущенные на пользователя токены и вернуть ошибку
        if await check_revoked(payload['jti']):
            await IssuedJWTToken.filter(subject=user).update(revoked=True)
            return None, AccessError.get_token_already_revoked_error()

        device_id = payload['device_id']
        await IssuedJWTToken.filter(subject=user, device_id=device_id).update(revoked=True)

        access_token, refresh_token = await self._issue_tokens_for_user(user, device_id)

        return TokensDTO(access_token=access_token, refresh_token=refresh_token), None

    async def _issue_tokens_for_user(self, user: APIUser, device_id: str = generate_device_id()) -> tuple[str, str]:
        access_token = self._jwt_auth.generate_access_token(subject=str(user.id), payload={'device_id': device_id})
        refresh_token = self._jwt_auth.generate_refresh_token(subject=str(user.id), payload={'device_id': device_id})

        raw_tokens = [self._jwt_auth.get_raw_jwt(token) for token in [access_token, refresh_token]]

        await IssuedJWTToken.bulk_create(
            [
                IssuedJWTToken(
                    subject=user,
                    jti=token_payload['jti'],
                    device_id=device_id,
                    expired_time=token_payload['exp']
                )
                for token_payload in raw_tokens
            ]
        )

        return access_token, refresh_token
