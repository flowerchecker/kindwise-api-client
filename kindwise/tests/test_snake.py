from kindwise.models import Identification
from .conftest import run_test_requests_to_server, IMAGE_DIR, run_test_available_details
from ..snake import SnakeApi


def test_requests_to_insect_server(api_key):
    run_test_requests_to_server(SnakeApi(api_key=api_key), 'snake', IMAGE_DIR / 'naja_subfulva.png', Identification)


def test_available_details(api_key):
    expected_view_names = {
        'common_names',
        'danger',
        'description',
        'fangs',
        'gbif_id',
        'image',
        'images',
        'inaturalist_id',
        'length',
        'number_of_species',
        'range',
        'rank',
        'rarity',
        'synonyms',
        'taxonomy',
        'url',
    }
    expected_license = {'description', 'image', 'images'}
    expected_localized = {'common_names', 'url', 'description'}

    run_test_available_details(
        expected_view_names, expected_license, expected_localized, SnakeApi(api_key=api_key).available_details()
    )
