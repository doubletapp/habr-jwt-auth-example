import pytest
from httpx import AsyncClient

from app.internal.users.models import APIUser
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.auth.middlewares.jwt.errors import AccessError
from app.pkg.auth.middlewares.jwt.utils import check_revoked, generate_device_id
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.auth.service import AuthService
from app.pkg.auth.tests.update_tokens.utils import issue_tokens
from app.pkg.for_tests.utils import create_user, faker, compare_error, issue_fake_access_token_for_user
from config.settings import jwt_config


@pytest.mark.anyio
async def test_update_tokens__invalid_refresh_token_error(client: AsyncClient) -> None:
    user = await create_user()
    access_token = issue_fake_access_token_for_user(user=user)

    data = {'refresh_token': faker.pystr()}

    response = await client.post(
        url='/api/auth/update-tokens',
        headers={'Authorization': f'Bearer {access_token}'},
        json=data,
    )

    assert response.status_code == 400

    response_data = response.json()

    compare_error(response_data, AccessError.get_invalid_token_error())


@pytest.mark.anyio
async def test_update_tokens__invalid_token_type_error(client: AsyncClient) -> None:
    user = await create_user()
    access_token = issue_fake_access_token_for_user(user=user)

    data = {'refresh_token': access_token}

    response = await client.post(
        url='/api/auth/update-tokens',
        headers={'Authorization': f'Bearer {access_token}'},
        json=data,
    )

    assert response.status_code == 400

    response_data = response.json()

    compare_error(response_data, AccessError.get_incorrect_token_type_error())


@pytest.mark.anyio
async def test_update_tokens__already_updated_token_error(client: AsyncClient) -> None:
    jwt_auth = JWTAuth(jwt_config)

    user = await create_user()

    access_token, refresh_token = await issue_tokens(jwt_auth=jwt_auth, user=user)

    await IssuedJWTToken.filter(jti=jwt_auth.get_jti(token=refresh_token)).update(revoked=True)

    response = await client.post(
        url='/api/auth/update-tokens',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'refresh_token': refresh_token},
    )

    assert response.status_code == 400

    response_data = response.json()
    compare_error(response_data, AccessError.get_token_already_revoked_error())

    for jti in [jwt_auth.get_jti(token=token) for token in [access_token, refresh_token]]:
        assert await check_revoked(jti)
