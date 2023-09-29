import pytest
from httpx import AsyncClient

from app.internal.users.models import APIUser
from app.pkg.for_tests.utils import check_oauth_token
from app.pkg.utils import get_sha256_hash


@pytest.mark.anyio
async def test_register__success(client: AsyncClient, user_credentials_data: dict[str, str]) -> None:
    response = await client.post(url='/api/auth/register', json=user_credentials_data)

    assert response.status_code == 200

    assert await APIUser.filter(
        email=user_credentials_data['email'],
        password_hash=get_sha256_hash(line=user_credentials_data['password']),
    ).exists()

    response_data = response.json()

    await check_oauth_token(token=response_data['access_token'])
    await check_oauth_token(token=response_data['refresh_token'])
