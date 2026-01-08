import pytest
from kindwise.async_api.mushroom import AsyncMushroomApi
from kindwise.models import Identification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server, run_test_available_details


@pytest.mark.asyncio
async def test_requests_to_mushroom_server(api_key):
    await run_async_test_requests_to_server(
        AsyncMushroomApi(api_key=api_key), 'mushroom', IMAGE_DIR / 'amanita_muscaria.jpg', Identification
    )


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'url',
        'description',
        'edibility',
        'psychoactive',
        'characteristic',
        'look_alike',
        'taxonomy',
        'rank',
        'gbif_id',
        'inaturalist_id',
        'image',
        'images',
    }
    expected_license = {'description', 'image', 'images'}
    expected_localized = {'common_names', 'url', 'description'}

    run_test_available_details(
        expected_view_names, expected_license, expected_localized, AsyncMushroomApi(api_key=api_key).available_details()
    )
