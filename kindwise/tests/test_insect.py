import base64
from datetime import datetime

import pytest

from kindwise.insect import InsectApi
from kindwise.models import Identification, Result, Input, Classification, Suggestion, SimilarImage
from .conftest import IMAGE_DIR, staging_api


@pytest.fixture
def api(api_key):
    api_ = InsectApi(api_key=api_key)
    return api_


@pytest.fixture
def identification():
    return Identification(
        access_token='TDp7etcIfwK8LCh',
        model_version='insect_id:1.0.1',
        custom_id=None,
        input=Input(
            images=['https://insect.kindwise.com/media/images/2acb5cf7bd7a48b2afda07ef54f42e16.jpg'],
            datetime=datetime.fromisoformat('2023-11-22T08:49:26.136448+00:00'),
            latitude=None,
            longitude=None,
            similar_images=True,
        ),
        result=Result(
            classification=Classification(
                suggestions=[
                    Suggestion(
                        id='3a16a1c61de4d33b',
                        name='Osmia ' 'bicornis',
                        probability=0.9998153,
                        similar_images=[
                            SimilarImage(
                                id='08d93df0e7ecc5391d18be8e645a6baa',
                                url='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.jpeg',
                                similarity=0.707,
                                url_small='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.small.jpeg',
                                license_name='CC ' 'BY ' '4.0',
                                license_url='https://creativecommons.org/licenses/by/4.0/',
                                citation='Maarten ' 'Trekels',
                            ),
                            SimilarImage(
                                id='c9b945dda9d60950972250171bf31808',
                                url='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.jpeg',
                                similarity=0.698,
                                url_small='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.small.jpeg',
                                license_name='CC BY 4.0',
                                license_url='https://creativecommons.org/licenses/by/4.0/',
                                citation='John ' 'Forrester',
                            ),
                        ],
                        details={'entity_id': '3a16a1c61de4d33b', 'language': 'en'},
                    )
                ]
            )
        ),
        status='COMPLETED',
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1700642966.136448),
        completed=datetime.fromtimestamp(1700642966.580449),
    )


@pytest.fixture
def identification_dict():
    return {
        'access_token': 'TDp7etcIfwK8LCh',
        'completed': 1700642966.580449,
        'created': 1700642966.136448,
        'custom_id': None,
        'input': {
            'datetime': '2023-11-22T08:49:26.136448+00:00',
            'images': ['https://insect.kindwise.com/media/images/2acb5cf7bd7a48b2afda07ef54f42e16.jpg'],
            'latitude': None,
            'longitude': None,
            'similar_images': True,
        },
        'model_version': 'insect_id:1.0.1',
        'result': {
            'classification': {
                'suggestions': [
                    {
                        'details': {'entity_id': '3a16a1c61de4d33b', 'language': 'en'},
                        'id': '3a16a1c61de4d33b',
                        'name': 'Osmia bicornis',
                        'probability': 0.9998153,
                        'similar_images': [
                            {
                                'citation': 'Maarten ' 'Trekels',
                                'id': '08d93df0e7ecc5391d18be8e645a6baa',
                                'license_name': 'CC ' 'BY ' '4.0',
                                'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                                'similarity': 0.707,
                                'url': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.jpeg',
                                'url_small': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.small.jpeg',
                            },
                            {
                                'citation': 'John ' 'Forrester',
                                'id': 'c9b945dda9d60950972250171bf31808',
                                'license_name': 'CC ' 'BY ' '4.0',
                                'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                                'similarity': 0.698,
                                'url': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.jpeg',
                                'url_small': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.small.jpeg',
                            },
                        ],
                    }
                ]
            }
        },
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'status': 'COMPLETED',
    }


@pytest.fixture
def image_path():
    return IMAGE_DIR / 'bee.jpeg'


@pytest.fixture
def image_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def test_identify(api, api_key, identification, identification_dict, image_path, image_base64, requests_mock):
    requests_mock.post(
        f'{api.identification_url}',
        json=identification_dict,
    )
    response_identification = api.identify(image_path)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'images': [image_base64], 'similar_images': True}
    assert response_identification == identification

    response_identification = api.identify(image_path, as_dict=True)
    request_record = requests_mock.request_history.pop()
    assert response_identification == identification_dict

    response_identification = api.identify(
        image_path, similar_images=False, details=['image'], language='cz', latitude_longitude=(1.0, 2.0)
    )
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}?details=image&language=cz'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {
        'images': [image_base64],
        'similar_images': False,
        'latitude': 1.0,
        'longitude': 2.0,
    }

    api.identify(image_path, language=['cz', 'de'])
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}?language=cz,de'

    api.identify([image_path, image_path])
    request_record = requests_mock.request_history.pop()
    assert request_record.json() == {
        'images': [image_base64, image_base64],
        'similar_images': True,
    }

    api.identify(image_path, details='image')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}?details=image'

    api.identify(image_path, asynchronous=True)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}?async=true'


def test_get_identification(api, api_key, identification, identification_dict, image_path, requests_mock):
    requests_mock.get(
        f'{api.identification_url}/{identification.access_token}',
        json=identification_dict,
    )
    response_identification = api.get_identification(identification.access_token)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response_identification == identification

    response_identification = api.get_identification(identification.access_token, as_dict=True)
    request_record = requests_mock.request_history.pop()
    assert response_identification == identification_dict

    response_identification = api.get_identification(identification.access_token, details=['image'], language='cz')
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}?details=image&language=cz'

    api.get_identification(identification.access_token, language=['cz', 'de'])
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{identification.access_token}?language=cz,de'

    api.get_identification(identification.access_token, details='image')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{identification.access_token}?details=image'

    api.get_identification(identification.access_token, details='image,images')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{identification.access_token}?details=image,images'


def test_delete_identification(api, api_key, identification, requests_mock):
    requests_mock.delete(
        f'{api.identification_url}/{identification.access_token}',
        json=True,
    )
    response = api.delete_identification(identification.access_token)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'DELETE'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response


def test_usage(api, api_key, usage_info, usage_info_dict, requests_mock):
    requests_mock.get(
        api.usage_info_url,
        json=usage_info_dict,
    )
    response = api.usage_info()
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.usage_info_url}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response == usage_info

    response = api.usage_info(as_dict=True)
    assert response == usage_info_dict


def test_feedback(api, api_key, identification, requests_mock):
    requests_mock.post(
        f'{api.identification_url}/{identification.access_token}/feedback',
        json={},
    )
    response = api.feedback(identification.access_token, comment='correct', rating=5)
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}/feedback'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'comment': 'correct', 'rating': 5}
    assert response

    response = api.feedback(identification.access_token, rating=5)
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}/feedback'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'rating': 5}
    assert response

    response = api.feedback(identification.access_token, comment='correct')
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}/feedback'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'comment': 'correct'}
    assert response

    with pytest.raises(ValueError, match='Either comment or rating must be provided'):
        api.feedback(identification.access_token)


def test_requests_to_server(api, image_path):
    with staging_api(api, 'insect') as api:
        usage_info = api.usage_info()

        identification = api.identify(image_path, latitude_longitude=(1.0, 2.0), asynchronous=True)
        assert isinstance(identification, Identification)

        api.feedback(identification.access_token, comment='correct', rating=5)

        identification = api.get_identification(identification.access_token, details=['image'], language='cz')
        assert isinstance(identification, Identification)
        assert 'image' in identification.result.classification.suggestions[0].details
        assert identification.result.classification.suggestions[0].details['language'] == 'cz'
        assert api.delete_identification(identification.access_token)

        with pytest.raises(ValueError):
            api.get_identification(identification.access_token)
