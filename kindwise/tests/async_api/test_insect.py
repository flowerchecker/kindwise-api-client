import pytest
from kindwise.async_api.insect import AsyncInsectApi
from kindwise.models import Identification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server, run_test_available_details


@pytest.mark.asyncio
async def test_requests_to_insect_server(api_key):
    await run_async_test_requests_to_server(
        AsyncInsectApi(api_key=api_key), 'insect', IMAGE_DIR / 'bee.jpeg', Identification
    )


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'danger',
        'danger_description',
        'description',
        'gbif_id',
        'image',
        'images',
        'inaturalist_id',
        'rank',
        'red_list',
        'role',
        'synonyms',
        'taxonomy',
        'url',
    }
    expected_license = {'description', 'image', 'images'}
    expected_localized = {'common_names', 'url', 'description'}

    run_test_available_details(
        expected_view_names, expected_license, expected_localized, AsyncInsectApi(api_key=api_key).available_details()
    )
