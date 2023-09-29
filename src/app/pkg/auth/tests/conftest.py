import pytest

from app.pkg.for_tests.utils import faker


@pytest.fixture(scope='function')
def user_credentials_data() -> dict[str, str]:
    return {
        'email': faker.email(),
        'password': faker.password(),
    }
