from kindwise.models import Identification
from .conftest import run_test_requests_to_server, IMAGE_DIR
from ..mushroom import MushroomApi


def test_requests_to_mushroom_server(api_key):
    run_test_requests_to_server(
        MushroomApi(api_key=api_key), 'mushroom', IMAGE_DIR / 'amanita_muscaria.jpg', Identification
    )
