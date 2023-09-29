import pytest
from httpx import AsyncClient
from app.internal.users.models import APIUser
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth

from app.pkg.auth.middlewares.jwt.errors import AccessError
from app.pkg.auth.middlewares.jwt.utils import generate_device_id
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.for_tests.utils import create_user, faker, compare_error
from config.settings import jwt_config


HANDLERS = [
    ('post', '/api/auth/logout'),
    ('post', '/api/auth/update-tokens'),
    ('get', '/api/me'),
]


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__token_is_not_specified_error(client: AsyncClient, method: str, url: str) -> None:
    response = await getattr(client, method)(url=url)

    assert response.status_code == 400

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_token_is_not_specified_error(),
    )


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__incorrect_auth_header_form_error(client: AsyncClient, method: str, url: str) -> None:
    response = await getattr(client, method)(
        url=url,
        headers={'Authorization': faker.pystr()},
    )

    assert response.status_code == 400

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_incorrect_auth_header_form_error(),
    )


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__invalid_token_error(client: AsyncClient, method: str, url: str) -> None:
    response = await getattr(client, method)(
        url=url,
        headers={'Authorization': f'Bearer {faker.pystr()}'},
    )

    assert response.status_code == 403

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_invalid_token_error(),
    )


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__incorrect_token_type_error(client: AsyncClient, method: str, url: str) -> None:
    jwt_auth = JWTAuth(config=jwt_config)

    user = await create_user()

    response = await getattr(client, method)(
        url=url,
        headers={'Authorization': f'Bearer {jwt_auth.generate_refresh_token(subject=str(user.id))}'},
    )

    assert response.status_code == 403

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_incorrect_token_type_error(),
    )


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__token_revoked_error(client: AsyncClient, method: str, url: str) -> None:
    jwt_auth = JWTAuth(config=jwt_config)

    user = await create_user()

    token = await _get_revoked_token(jwt_auth=jwt_auth, user=user)

    response = await getattr(client, method)(
        url=url,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 403

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_token_revoked_error(),
    )


@pytest.mark.anyio
@pytest.mark.parametrize('method, url', HANDLERS)
async def test_access_check__token_owner_not_found(client: AsyncClient, method: str, url: str) -> None:
    jwt_auth = JWTAuth(config=jwt_config)

    user = await create_user()

    token = jwt_auth.generate_access_token(subject=str(user.id))

    await user.delete()

    response = await getattr(client, method)(
        url=url,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 403

    response_data = response.json()

    compare_error(
        error_in_response=response_data,
        error=AccessError.get_token_owner_not_found(),
    )


async def _get_revoked_token(jwt_auth: JWTAuth, user: APIUser) -> str:
    device_id = generate_device_id()

    token = jwt_auth.generate_access_token(subject=str(user.id), payload={'device_id': device_id})

    token_payload = jwt_auth.get_raw_jwt(token)

    await IssuedJWTToken.create(
        subject=user,
        jti=token_payload['jti'],
        device_id=device_id,
        expired_time=token_payload['exp'],
        revoked=True,
    )

    return token
