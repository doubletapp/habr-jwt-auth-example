import pytest
from httpx import AsyncClient

from app.internal.users.models import APIUser
from app.pkg.auth.errors import AuthError
from app.pkg.for_tests.utils import compare_error, create_user


@pytest.mark.anyio
async def test_register__email_occupied_error(client: AsyncClient, user_credentials_data: dict[str, str]) -> None:
    await create_user(email=user_credentials_data['email'])

    response = await client.post(url='/api/auth/register', json=user_credentials_data)

    assert response.status_code == 400

    response_data = response.json()

    compare_error(response_data, AuthError.get_email_occupied_error())
