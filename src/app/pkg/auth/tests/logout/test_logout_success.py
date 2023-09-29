import jwt
import pytest

from app.conftest import AsyncClient
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.auth.middlewares.jwt.utils import check_revoked
from app.pkg.for_tests.utils import create_user, issue_fake_access_token_for_user
from config.settings import jwt_config


@pytest.mark.anyio
async def test_logout__success(client: AsyncClient) -> None:
    user = await create_user()

    token = issue_fake_access_token_for_user(user=user)
    payload = jwt.decode(jwt=token, key=jwt_config.secret, algorithms=['HS256', 'RS256'])
    await IssuedJWTToken.create(jti=payload['jti'], subject=user, device_id=payload['device_id'], revoked=False)

    response = await client.post(
        url='/api/auth/logout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data['success']

    assert await check_revoked(payload['jti'])
