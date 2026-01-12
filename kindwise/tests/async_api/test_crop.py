import pytest

from kindwise.async_api.crop_health import AsyncCropHealthApi, CropIdentification
from kindwise.tests.conftest import IMAGE_DIR, run_async_test_requests_to_server


@pytest.mark.asyncio
async def test_requests_to_crop_server(api_key):
    await run_async_test_requests_to_server(
        AsyncCropHealthApi(api_key=api_key),
        'crop',
        IMAGE_DIR / 'potato.late_blight.jpg',
        CropIdentification,
        model_name='disease',
    )
