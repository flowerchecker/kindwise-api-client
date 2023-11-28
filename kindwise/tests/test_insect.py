from kindwise.models import Identification
from .conftest import run_test_requests_to_server, IMAGE_DIR
from ..insect import InsectApi


def test_requests_to_insect_server(api_key):
    run_test_requests_to_server(InsectApi(api_key=api_key), 'insect', IMAGE_DIR / 'bee.jpeg', Identification)
