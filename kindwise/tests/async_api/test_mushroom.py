import pytest
from kindwise.async_api.mushroom import AsyncMushroomApi
from kindwise.models import Identification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server


@pytest.mark.asyncio
async def test_requests_to_mushroom_server(api_key):
    await run_async_test_requests_to_server(
        AsyncMushroomApi(api_key=api_key), 'mushroom', IMAGE_DIR / 'amanita_muscaria.jpg', Identification
    )
