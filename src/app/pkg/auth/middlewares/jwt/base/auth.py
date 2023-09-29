import jwt
import uuid
from typing import Any
from datetime import datetime, timedelta, timezone

from app.pkg.auth.middlewares.jwt.base.config import JWTConfig
from app.pkg.auth.middlewares.jwt.base.token_types import TokenType
from app.pkg.utils import convert_to_timestamp


class JWTAuth:
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    def generate_unlimited_access_token(self, subject: str, payload: dict[str, Any] = {}) -> str:
        return self.__sign_token(type=TokenType.ACCESS.value, subject=subject, payload=payload)

    def generate_access_token(self, subject: str, payload: dict[str, Any] = {}) -> str:
        return self.__sign_token(
            type=TokenType.ACCESS.value,
            subject=subject,
            payload=payload,
            ttl=self._config.access_token_ttl,
        )

    def generate_refresh_token(self, subject: str, payload: dict[str, Any] = {}) -> str:
        return self.__sign_token(
            type=TokenType.REFRESH.value,
            subject=subject,
            payload=payload,
            ttl=self._config.refresh_token_ttl,
        )

    def __sign_token(self, type: str, subject: str, payload: dict[str, Any] = {}, ttl: timedelta = None) -> str:
        current_timestamp = convert_to_timestamp(datetime.now(tz=timezone.utc))

        data = dict(
            iss='befunny@auth_service',
            sub=subject,
            type=type,
            jti=self.__generate_jti(),
            iat=current_timestamp,
            nbf=payload['nbf'] if payload.get('nbf') else current_timestamp,
        )
        data.update(dict(exp=data['nbf'] + int(ttl.total_seconds()))) if ttl else None
        payload.update(data)
        return jwt.encode(payload, self._config.secret, algorithm=self._config.algorithm)

    @staticmethod
    def __generate_jti() -> str:
        return str(uuid.uuid4())

    def verify_token(self, token) -> dict[str, Any]:
        return jwt.decode(token, self._config.secret, algorithms=[self._config.algorithm])

    def get_jti(self, token) -> str:
        return self.verify_token(token)['jti']

    def get_sub(self, token) -> str:
        return self.verify_token(token)['sub']

    def get_exp(self, token) -> int:
        return self.verify_token(token)['exp']

    @staticmethod
    def get_raw_jwt(token) -> dict[str, Any]:
        """
        Return the payload of the token without checking the validity of the token
        """
        return jwt.decode(token, options={'verify_signature': False})
