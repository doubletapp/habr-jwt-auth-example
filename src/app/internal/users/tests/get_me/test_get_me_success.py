import pytest
from httpx import AsyncClient

from app.internal.users.models import APIUser
from app.pkg.for_tests.utils import create_user, issue_fake_access_token_for_user
from app.pkg.utils import get_sha256_hash


@pytest.mark.anyio
async def test_get_me__success(client: AsyncClient) -> None:
    user = await create_user()

    token = issue_fake_access_token_for_user(user=user)
    response = await client.get(
        url='/api/me',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200

    response_data = response.json()

    _compare_users(user_in_response=response_data, user_in_db=user)


def _compare_users(user_in_response: dict[str, str], user_in_db: APIUser) -> None:
    assert user_in_response['id'] == str(user_in_db.id)
    assert user_in_response['email'] == user_in_db.email
