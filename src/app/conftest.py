import pytest
from _pytest.fixtures import SubRequest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

from config.settings import TORTOISE_ORM, switch_to_test_mode

switch_to_test_mode()

from app.internal.main import app  # noqa: E402


@pytest.fixture(scope='session', autouse=True)
def initialize_tests(request: SubRequest) -> None:
    initializer(
        modules=TORTOISE_ORM['apps']['models']['models'],
        db_url=TORTOISE_ORM['connections']['default'],
        app_label='models',
    )
    request.addfinalizer(finalizer)


@pytest.fixture(scope='module')
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='module')
async def client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            yield client
