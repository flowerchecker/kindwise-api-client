from kindwise.models import Identification
from .conftest import run_test_requests_to_server, IMAGE_DIR, run_test_available_details
from ..insect import InsectApi


def test_requests_to_insect_server(api_key):
    run_test_requests_to_server(InsectApi(api_key=api_key), 'insect', IMAGE_DIR / 'bee.jpeg', Identification)


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'url',
        'description',
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
        expected_view_names, expected_license, expected_localized, InsectApi(api_key=api_key).available_details()
    )
