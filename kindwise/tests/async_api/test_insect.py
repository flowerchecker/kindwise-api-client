import pytest
from kindwise.async_api.insect import AsyncInsectApi
from kindwise.models import Identification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server


@pytest.mark.asyncio
async def test_requests_to_insect_server(api_key):
    await run_async_test_requests_to_server(
        AsyncInsectApi(api_key=api_key), 'insect', IMAGE_DIR / 'bee.jpeg', Identification
    )
