import pytest
from httpx import AsyncClient

from app.internal.users.models import APIUser
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.middlewares.jwt.errors import AccessError
from app.pkg.auth.middlewares.jwt.utils import check_revoked, generate_device_id
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.auth.service import AuthService
from app.pkg.for_tests.utils import check_oauth_token, create_user, faker, compare_error, issue_fake_access_token_for_user
from app.pkg.auth.tests.update_tokens.utils import issue_tokens
from config.settings import jwt_config


@pytest.mark.anyio
async def test_update_tokens__success(client: AsyncClient) -> None:
    jwt_auth = JWTAuth(jwt_config)

    user = await create_user()

    access_token, refresh_token = await issue_tokens(jwt_auth=jwt_auth, user=user)

    response = await client.post(
        url='/api/auth/update-tokens',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'refresh_token': refresh_token},
    )

    assert response.status_code == 200

    assert await check_revoked(jwt_auth.get_jti(token=access_token))
    assert await check_revoked(jwt_auth.get_jti(token=refresh_token))

    response_data = response.json()
    
    await check_oauth_token(token=response_data['access_token'])
    await check_oauth_token(token=response_data['refresh_token'])
