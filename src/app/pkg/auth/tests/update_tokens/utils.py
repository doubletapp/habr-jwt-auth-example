from app.internal.users.models import APIUser
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.service import AuthService


async def issue_tokens(jwt_auth: JWTAuth, user: APIUser) -> tuple[str, str]:
    return await AuthService(jwt_auth=jwt_auth)._issue_tokens_for_user(user=user)
