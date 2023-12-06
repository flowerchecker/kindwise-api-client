import os
import random
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from kindwise.models import UsageInfo

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


def run_test_requests_to_server(api, system_name, image_path, identification_type):
    assert system_name.lower() in ['insect', 'mushroom', 'plant']
    with staging_api(api, system_name) as api:
        usage_info = api.usage_info()
        print('Usage info:')
        print(usage_info)
        print()

        custom_id = random.randint(1000000, 2000000)
        date_time = datetime.now()
        identification = api.identify(
            image_path, latitude_longitude=(1.0, 2.0), asynchronous=True, custom_id=custom_id, date_time=date_time
        )
        assert isinstance(identification, identification_type)
        print(f'Identification created with async, {date_time=} and {custom_id=}:')
        print(identification)
        print()
        assert api.feedback(identification.access_token, comment='correct', rating=5)

        identification = api.get_identification(identification.access_token, details=['image'], language='cz')
        print('Identification with image details, custom id and cz language:')
        print(identification)
        assert isinstance(identification, identification_type)
        assert 'image' in identification.result.classification.suggestions[0].details
        assert identification.result.classification.suggestions[0].details['language'] == 'cz'
        assert identification.feedback.comment == 'correct'
        assert identification.feedback.rating == 5
        assert identification.custom_id == custom_id
        assert identification.input.datetime == date_time

        assert api.delete_identification(identification.access_token)

        with pytest.raises(ValueError):
            api.get_identification(identification.access_token)


class RequestMatcher:
    def __init__(self, api, api_key, image_path, requests_mock, identification_dict, identification):
        self.api = api
        self.api_key = api_key
        self.image_path = image_path
        self.requests_mock = requests_mock
        self.identification_dict = identification_dict
        self.identification = identification
        self.requests_mock.post(
            f'{self.api.identification_url}',
            json=identification_dict,
        )
        self.requests_mock.get(
            f'{api.identification_url}/{identification_dict["access_token"]}',
            json=identification_dict,
        )

    def check_identify_request(
        self,
        expected_payload: list[tuple[str, str]] = None,
        expected_query: str = None,
        expected_result=None,
        raises: type[Exception] = None,
        **kwargs,
    ):
        if raises is None:
            if 'image' not in kwargs:
                kwargs['image'] = self.image_path
            response = self.api.identify(**kwargs)
        else:
            with pytest.raises(raises):
                self.api.identify(self.image_path, **kwargs)
            return
        request_record = self.requests_mock.request_history.pop()
        assert request_record.method == 'POST'
        assert request_record.headers['Content-Type'] == 'application/json'
        assert request_record.headers['Api-Key'] == self.api_key
        if expected_query is not None:
            if not expected_query.startswith('?') and len(expected_query) > 0:
                expected_query = '?' + expected_query
            assert request_record.url == f'{self.api.identification_url}{expected_query}'
        if expected_payload is not None:
            payload = request_record.json()
            for key, value in expected_payload:
                assert payload[key] == value
        if expected_result is not None:
            assert response == expected_result

    def check_get_identification_request(self, expected_query: str = None, **kwargs):
        response_identification = self.api.get_identification(self.identification_dict['access_token'], **kwargs)
        assert len(self.requests_mock.request_history) == 1
        request_record = self.requests_mock.request_history.pop()
        assert request_record.method == 'GET'
        assert request_record.headers['Content-Type'] == 'application/json'
        assert request_record.headers['Api-Key'] == self.api_key
        if expected_query is not None:
            if not expected_query.startswith('?'):
                expected_query = '?' + expected_query
                assert (
                    request_record.url
                    == f'{self.api.identification_url}/{self.identification_dict["access_token"]}{expected_query}'
                )
        assert response_identification == self.identification


@pytest.fixture
def request_matcher(api, api_key, image_path, requests_mock, identification_dict, identification):
    return RequestMatcher(api, api_key, image_path, requests_mock, identification_dict, identification)


@pytest.fixture
def usage_info_dict():
    return {
        "active": True,
        "credit_limits": {"day": None, "week": None, "month": None, "total": 100},
        "used": {"day": 1, "week": 1, "month": 1, "total": 2},
        "can_use_credits": {"value": True, "reason": None},
        "remaining": {"day": None, "week": None, "month": None, "total": 98},
    }


@pytest.fixture
def usage_info(usage_info_dict):
    return UsageInfo.from_dict(usage_info_dict)


def run_test_available_details(expected_view_names, expected_license, expected_localized, available_views):
    assert expected_view_names == {v['name'] for v in available_views}
    assert expected_license == {v['name'] for v in available_views if v['license']}
    assert expected_localized == {v['name'] for v in available_views if v['localized']}
