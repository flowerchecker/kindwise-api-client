import pytest

from kindwise.async_api.crop_health import AsyncCropHealthApi, CropIdentification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server, run_test_available_details


@pytest.mark.asyncio
def test_requests_to_crop_server(api_key):
    run_async_test_requests_to_server(
        AsyncCropHealthApi(api_key=api_key),
        'crop',
        IMAGE_DIR / 'potato.late_blight.jpg',
        CropIdentification,
        model_name='disease',
    )


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'description',
        'eppo_code',
        'eppo_regulation_status',
        'gbif_id',
        'image',
        'images',
        'severity',
        'spreading',
        'symptoms',
        'taxonomy',
        'treatment',
        'type',
        'wiki_description',
        'wiki_url',
    }
    expected_license = {'wiki_description', 'image', 'images'}
    expected_localized = {'common_names', 'wiki_url', 'wiki_description'}

    run_test_available_details(
        expected_view_names,
        expected_license,
        expected_localized,
        AsyncCropHealthApi(api_key=api_key).available_details(),
    )
