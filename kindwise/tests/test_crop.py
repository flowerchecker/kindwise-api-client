from .conftest import run_test_requests_to_server, IMAGE_DIR, run_test_available_details, skip_integration_tests
from .. import CropHealthApi
from ..crop_health import CropIdentification


@skip_integration_tests
def test_requests_to_crop_server(api_key):
    run_test_requests_to_server(
        CropHealthApi(api_key=api_key),
        'crop',
        IMAGE_DIR / 'potato.late_blight.jpg',
        CropIdentification,
        model_name='disease',
    )


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'type',
        'wiki_url',
        'wiki_description',
        'taxonomy',
        'eppo_code',
        'gbif_id',
        'image',
        'images',
        'eppo_regulation_status',
    }
    expected_license = {'wiki_description', 'image', 'images'}
    expected_localized = {'common_names', 'wiki_url', 'wiki_description'}

    run_test_available_details(
        expected_view_names, expected_license, expected_localized, CropHealthApi(api_key=api_key).available_details()
    )
