from typing import Callable
import pytest
from httpx import AsyncClient

from app.pkg.auth.errors import AuthError
from app.pkg.for_tests.utils import create_user, faker, compare_error
from app.pkg.utils import get_sha256_hash


async def __get_credentials_with_invalid_email() -> dict[str, str]:
    password = faker.password()

    await create_user(password_hash=get_sha256_hash(line=password))

    return {'email': faker.email(), 'password': password}


async def __get_credentials_with_invalid_password() -> dict[str, str]:
    email = faker.email()

    await create_user(email=email)

    return {'email': email, 'password': faker.password()}


@pytest.mark.anyio
@pytest.mark.parametrize(
    'func_for_get_user_credentials_data',
    [
        __get_credentials_with_invalid_email,
        __get_credentials_with_invalid_password
    ]
)
async def test_login__invalid_credentials_error(client: AsyncClient, func_for_get_user_credentials_data: Callable) -> None:
    user_credentials_data = await func_for_get_user_credentials_data()

    response = await client.post(url='/api/auth/login', json=user_credentials_data)

    assert response.status_code == 400

    response_data = response.json()

    compare_error(response_data, AuthError.get_invalid_credentials_error())
