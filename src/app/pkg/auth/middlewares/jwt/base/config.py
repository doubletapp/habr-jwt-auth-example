from dataclasses import dataclass
from datetime import timedelta


@dataclass
class JWTConfig:
    secret: str
    algorithm: str = 'HS256'
    access_token_ttl: timedelta = None
    refresh_token_ttl: timedelta = None
