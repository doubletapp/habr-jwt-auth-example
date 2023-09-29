from faker import Faker
from datetime import datetime, timezone
from app.internal.users.models import APIUser

from app.pkg.auth.middlewares.jwt.utils import check_revoked, generate_device_id
from app.pkg.auth.models import IssuedJWTToken
from app.pkg.errors import ErrorObj
from app.pkg.auth.middlewares.jwt.base.auth import JWTAuth
from app.pkg.utils import convert_to_timestamp
from config.settings import jwt_config


faker = Faker()


def compare_error(error_in_response: dict[str, str], error: ErrorObj) -> None:
    assert error_in_response['type'] == error.type
    assert error_in_response['message'] == error.message


async def check_oauth_token(token: str) -> None:
    jwt_auth = JWTAuth(config=jwt_config)

    assert await IssuedJWTToken.filter(jti=jwt_auth.get_jti(token)).exists()

    decoded_access_token = jwt_auth.verify_token(token)

    assert not await check_revoked(decoded_access_token['jti'])

    assert decoded_access_token['iat'] == decoded_access_token['nbf']

    # With inaccuracy
    assert convert_to_timestamp(datetime.now(tz=timezone.utc)) - decoded_access_token['iat'] < 2


def issue_fake_access_token_for_user(user: APIUser) -> str:
    device_id = generate_device_id()
    jwt_auth = JWTAuth(config=jwt_config)
    return jwt_auth.generate_access_token(
        subject=str(user.id),
        payload={'device_id': device_id},
    )


async def create_user(**kwargs) -> APIUser:
    return await APIUser.create(**{'email': faker.email(), 'password_hash': faker.pystr(), **kwargs})
