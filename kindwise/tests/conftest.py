import os
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

TEST_DIR = Path(__file__).resolve().parent
IMAGE_DIR = TEST_DIR / 'resources' / 'images'
MOCK_REQUESTS = True


@pytest.fixture
def api_key():
    return 'b2a2f2c0-5e1a-4e4a-8b9a-5b6b0e2e2b9a'


@contextmanager
def staging_api(api, system):
    assert system.lower() in ['insect', 'mushroom', 'plant']
    staging_host = os.getenv(f'{system.upper()}_STAGING_HOST')
    assert staging_host is not None, f'{system.capitalize()}_STAGING_HOST is not set in .env file'
    api_key = os.getenv(f'{system.upper()}_STAGING_API_KEY')
    assert api_key is not None, f'{system.capitalize()}_STAGING_API_KEY is not set in .env file'
    with patch.object(api, 'host', staging_host):
        with patch.object(api, 'api_key', api_key):
            yield api
