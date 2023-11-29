import base64
import random
from datetime import datetime

import pytest

from kindwise.models import (
    Input,
    Classification,
    Suggestion,
    SimilarImage,
    PlantIdentification,
    PlantResult,
    ResultEvaluation,
    HealthAssessment,
    HealthAssessmentResult,
)
from .conftest import IMAGE_DIR, run_test_requests_to_server, staging_api
from ..core import InputType
from ..plant import PlantApi


@pytest.fixture
def api(api_key):
    api_ = PlantApi(api_key=api_key)
    return api_


@pytest.fixture
def identification():
    return PlantIdentification(
        access_token='biXpfz7Fbe6cNLw',
        model_version='plant_id:3.4.1',
        custom_id=None,
        input=Input(
            images=['https://plant.id/media/imgs/87fd66a519c648deb8615c30fa734709.jpg'],
            datetime=datetime.fromisoformat('2023-11-28T08:38:48.538187+00:00'),
            latitude=None,
            longitude=None,
            similar_images=True,
        ),
        result=PlantResult(
            is_plant=ResultEvaluation(probability=1.0, binary=True, threshold=0.5),
            is_healthy=ResultEvaluation(probability=0.14163023233413696, binary=False, threshold=0.525),
            classification=Classification(
                suggestions=[
                    Suggestion(
                        id='4ba05f1050481731',
                        name='Aloe vera',
                        probability=0.9653021963116768,
                        similar_images=[
                            SimilarImage(
                                id='ac89509bf07b85d202d9f53094eea6394ce354c4',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.jpeg',
                                similarity=0.764,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.small.jpeg',
                            ),
                            SimilarImage(
                                id='d688b6a280e81d1a5b7bc2d0d2b8a1497f360551',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.jpeg',
                                similarity=0.707,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.small.jpeg',
                            ),
                        ],
                        details={'entity_id': '4ba05f1050481731', 'language': 'en'},
                    ),
                    Suggestion(
                        id='989a2d0dc4380c1c',
                        name='Bulbine',
                        probability=0.021534416819899538,
                        similar_images=[
                            SimilarImage(
                                id='d45aaf13e3b21eff2fecaf78c1fd04d9e38a634d',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d45/aaf13e3b21eff2fecaf78c1fd04d9e38a634d.jpeg',
                                similarity=0.469,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d45/aaf13e3b21eff2fecaf78c1fd04d9e38a634d.small.jpeg',
                                license_name='CC BY-SA 4.0',
                                license_url='https://creativecommons.org/licenses/by-sa/4.0/',
                                citation='Nicola van Berkel',
                            ),
                            SimilarImage(
                                id='f6083c8d5d41cadee61b2338c8f50d179ce8eb8e',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/f60/83c8d5d41cadee61b2338c8f50d179ce8eb8e.jpeg',
                                similarity=0.399,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/f60/83c8d5d41cadee61b2338c8f50d179ce8eb8e.small.jpeg',
                                license_name='CC BY 4.0',
                                license_url='https://creativecommons.org/licenses/by/4.0/',
                                citation='Matthew Fainman',
                            ),
                        ],
                        details={'entity_id': '989a2d0dc4380c1c', 'language': 'en'},
                    ),
                ]
            ),
            disease=Classification(
                suggestions=[
                    Suggestion(
                        id='e5eed7f688efa59e',
                        name='water excess or uneven watering',
                        probability=0.51401126,
                        similar_images=[
                            SimilarImage(
                                id='46d5fe95e07b0eddbe87446b7144c5c6bcc934c6',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.jpg',
                                similarity=0.614,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.small.jpg',
                            ),
                            SimilarImage(
                                id='3052cde93a199143a72f0a2ab575e7458919e3a8',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.jpg',
                                similarity=0.469,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.small.jpg',
                            ),
                        ],
                        details={'language': 'en', 'entity_id': 'e5eed7f688efa59e'},
                    ),
                    Suggestion(
                        id='53aac959aba8302b',
                        name='mechanical damage',
                        probability=0.30839583,
                        similar_images=[
                            SimilarImage(
                                id='d2e69dde952294c01f79b390a0af0aadc5cbf339',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.jpg',
                                similarity=0.632,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.small.jpg',
                            ),
                            SimilarImage(
                                id='c327514db735ef0ead10964fdfd275e61fddc5d3',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.jpg',
                                similarity=0.521,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.small.jpg',
                            ),
                        ],
                        details={'language': 'en', 'entity_id': '53aac959aba8302b'},
                    ),
                ]
            ),
        ),
        status='COMPLETED',
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1701160728.538187),
        completed=datetime.fromtimestamp(1701160729.289631),
        feedback=None,
    )


@pytest.fixture
def identification_dict():
    return {
        'access_token': 'biXpfz7Fbe6cNLw',
        'model_version': 'plant_id:3.4.1',
        'custom_id': None,
        'input': {
            'latitude': None,
            'longitude': None,
            'health': 'all',
            'similar_images': True,
            'images': ['https://plant.id/media/imgs/87fd66a519c648deb8615c30fa734709.jpg'],
            'datetime': '2023-11-28T08:38:48.538187+00:00',
        },
        'result': {
            'is_plant': {'probability': 1.0, 'binary': True, 'threshold': 0.5},
            'is_healthy': {'probability': 0.14163023233413696, 'binary': False, 'threshold': 0.525},
            'classification': {
                'suggestions': [
                    {
                        'id': '4ba05f1050481731',
                        'name': 'Aloe vera',
                        'probability': 0.9653021963116768,
                        'similar_images': [
                            {
                                'id': 'ac89509bf07b85d202d9f53094eea6394ce354c4',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.jpeg',
                                'similarity': 0.764,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.small.jpeg',
                            },
                            {
                                'id': 'd688b6a280e81d1a5b7bc2d0d2b8a1497f360551',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.jpeg',
                                'similarity': 0.707,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.small.jpeg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': '4ba05f1050481731'},
                    },
                    {
                        'id': '989a2d0dc4380c1c',
                        'name': 'Bulbine',
                        'probability': 0.021534416819899538,
                        'similar_images': [
                            {
                                'id': 'd45aaf13e3b21eff2fecaf78c1fd04d9e38a634d',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d45/aaf13e3b21eff2fecaf78c1fd04d9e38a634d.jpeg',
                                'license_name': 'CC BY-SA 4.0',
                                'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
                                'citation': 'Nicola van Berkel',
                                'similarity': 0.469,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d45/aaf13e3b21eff2fecaf78c1fd04d9e38a634d.small.jpeg',
                            },
                            {
                                'id': 'f6083c8d5d41cadee61b2338c8f50d179ce8eb8e',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/f60/83c8d5d41cadee61b2338c8f50d179ce8eb8e.jpeg',
                                'license_name': 'CC BY 4.0',
                                'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                                'citation': 'Matthew Fainman',
                                'similarity': 0.399,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/f60/83c8d5d41cadee61b2338c8f50d179ce8eb8e.small.jpeg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': '989a2d0dc4380c1c'},
                    },
                ]
            },
            'disease': {
                'suggestions': [
                    {
                        'id': 'e5eed7f688efa59e',
                        'name': 'water excess or uneven watering',
                        'probability': 0.51401126,
                        'similar_images': [
                            {
                                'id': '46d5fe95e07b0eddbe87446b7144c5c6bcc934c6',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.jpg',
                                'similarity': 0.614,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.small.jpg',
                            },
                            {
                                'id': '3052cde93a199143a72f0a2ab575e7458919e3a8',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.jpg',
                                'similarity': 0.469,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.small.jpg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': 'e5eed7f688efa59e'},
                    },
                    {
                        'id': '53aac959aba8302b',
                        'name': 'mechanical damage',
                        'probability': 0.30839583,
                        'similar_images': [
                            {
                                'id': 'd2e69dde952294c01f79b390a0af0aadc5cbf339',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.jpg',
                                'similarity': 0.632,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.small.jpg',
                            },
                            {
                                'id': 'c327514db735ef0ead10964fdfd275e61fddc5d3',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.jpg',
                                'similarity': 0.521,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.small.jpg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': '53aac959aba8302b'},
                    },
                ]
            },
        },
        'status': 'COMPLETED',
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'created': 1701160728.538187,
        'completed': 1701160729.289631,
    }


@pytest.fixture
def image_path():
    return IMAGE_DIR / 'aloe-vera.jpg'


@pytest.fixture
def image_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def test_identify(api, api_key, identification, identification_dict, image_path, image_base64, requests_mock):
    requests_mock.post(
        f'{api.identification_url}',
        json=identification_dict,
    )
    response_identification = api.identify(image_path, health=True)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'images': [image_base64], 'similar_images': True, 'health': 'all'}
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

    api.identify(image_path)
    request_record = requests_mock.request_history.pop()
    assert request_record.json() == {'images': [image_base64], 'similar_images': True}

    api.identify(image_path, custom_id=1)
    request_record = requests_mock.request_history.pop()
    assert request_record.json() == {'images': [image_base64], 'similar_images': True, 'custom_id': 1}

    date = '2023-11-28T08:38:48.538187+00:00'
    api.identify(image_path, date_time=date)
    request_record = requests_mock.request_history.pop()
    assert request_record.json() == {'images': [image_base64], 'similar_images': True, 'datetime': date}

    # accept image as a file object
    with open(image_path, 'rb') as f:
        api.identify(f, input_type=InputType.FILE)
        request_record = requests_mock.request_history.pop()
        assert request_record.json() == {
            'images': [image_base64],
            'similar_images': True,
        }

    # accept image as a byte stream
    with open(image_path, 'rb') as f:
        image = f.read()
        api.identify(image, InputType.STREAM)
        request_record = requests_mock.request_history.pop()
        assert request_record.json() == {
            'images': [image_base64],
            'similar_images': True,
        }


@pytest.fixture
def health_assessment():
    return HealthAssessment(
        access_token='qK3x9ygwxhsHpqh',
        model_version='plant_id:3.4.1',
        custom_id=None,
        input=Input(
            images=['https://plant.id/media/imgs/be1232d95e624214812009bb1a547e27.jpg'],
            datetime=datetime.fromisoformat('2023-11-28T10:19:19.169041+00:00'),
            latitude=None,
            longitude=None,
            similar_images=True,
        ),
        result=HealthAssessmentResult(
            is_plant=ResultEvaluation(probability=1.0, binary=True, threshold=0.5),
            is_healthy=ResultEvaluation(probability=0.14163005352020264, binary=False, threshold=0.525),
            disease=Classification(
                suggestions=[
                    Suggestion(
                        id='e5eed7f688efa59e',
                        name='water excess or uneven watering',
                        probability=0.5140113,
                        similar_images=[
                            SimilarImage(
                                id='46d5fe95e07b0eddbe87446b7144c5c6bcc934c6',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.jpg',
                                similarity=0.614,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.small.jpg',
                            ),
                            SimilarImage(
                                id='3052cde93a199143a72f0a2ab575e7458919e3a8',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.jpg',
                                similarity=0.469,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.small.jpg',
                            ),
                        ],
                        details={'language': 'en', 'entity_id': 'e5eed7f688efa59e'},
                    ),
                    Suggestion(
                        id='53aac959aba8302b',
                        name='mechanical damage',
                        probability=0.30839592,
                        similar_images=[
                            SimilarImage(
                                id='d2e69dde952294c01f79b390a0af0aadc5cbf339',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.jpg',
                                similarity=0.632,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.small.jpg',
                            ),
                            SimilarImage(
                                id='c327514db735ef0ead10964fdfd275e61fddc5d3',
                                url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.jpg',
                                similarity=0.521,
                                url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.small.jpg',
                            ),
                        ],
                        details={'language': 'en', 'entity_id': '53aac959aba8302b'},
                    ),
                ]
            ),
        ),
        status='COMPLETED',
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1701166759.169041),
        completed=datetime.fromtimestamp(1701166760.103572),
        feedback=None,
    )


@pytest.fixture
def health_assessment_dict():
    return {
        'access_token': 'qK3x9ygwxhsHpqh',
        'model_version': 'plant_id:3.4.1',
        'custom_id': None,
        'input': {
            'latitude': None,
            'longitude': None,
            'health': 'only',
            'similar_images': True,
            'images': ['https://plant.id/media/imgs/be1232d95e624214812009bb1a547e27.jpg'],
            'datetime': '2023-11-28T10:19:19.169041+00:00',
        },
        'result': {
            'is_plant': {'probability': 1.0, 'binary': True, 'threshold': 0.5},
            'is_healthy': {'probability': 0.14163005352020264, 'binary': False, 'threshold': 0.525},
            'disease': {
                'suggestions': [
                    {
                        'id': 'e5eed7f688efa59e',
                        'name': 'water excess or uneven watering',
                        'probability': 0.5140113,
                        'similar_images': [
                            {
                                'id': '46d5fe95e07b0eddbe87446b7144c5c6bcc934c6',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.jpg',
                                'similarity': 0.614,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/46d/5fe95e07b0eddbe87446b7144c5c6bcc934c6.small.jpg',
                            },
                            {
                                'id': '3052cde93a199143a72f0a2ab575e7458919e3a8',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.jpg',
                                'similarity': 0.469,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/305/2cde93a199143a72f0a2ab575e7458919e3a8.small.jpg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': 'e5eed7f688efa59e'},
                    },
                    {
                        'id': '53aac959aba8302b',
                        'name': 'mechanical damage',
                        'probability': 0.30839592,
                        'similar_images': [
                            {
                                'id': 'd2e69dde952294c01f79b390a0af0aadc5cbf339',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.jpg',
                                'similarity': 0.632,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d2e/69dde952294c01f79b390a0af0aadc5cbf339.small.jpg',
                            },
                            {
                                'id': 'c327514db735ef0ead10964fdfd275e61fddc5d3',
                                'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.jpg',
                                'similarity': 0.521,
                                'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c32/7514db735ef0ead10964fdfd275e61fddc5d3.small.jpg',
                            },
                        ],
                        'details': {'language': 'en', 'entity_id': '53aac959aba8302b'},
                    },
                ]
            },
        },
        'status': 'COMPLETED',
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'created': 1701166759.169041,
        'completed': 1701166760.103572,
    }


def test_health_assessment(
    api, api_key, image_path, image_base64, requests_mock, health_assessment_dict, health_assessment
):
    requests_mock.post(api.health_assessment_url, json=health_assessment_dict)
    response = api.health_assessment(image_path)
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.health_assessment_url}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'images': [image_base64], 'similar_images': True}
    assert response == health_assessment

    response = api.health_assessment(image_path, full_disease_list=True)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.health_assessment_url}?full_disease_list=true'

    response = api.health_assessment(
        image_path, full_disease_list=True, asynchronous=True, language=['cz', 'de'], details='image'
    )
    request_record = requests_mock.request_history.pop()
    assert (
        request_record.url
        == f'{api.health_assessment_url}?details=image&language=cz,de&async=true&full_disease_list=true'
    )
    assert request_record.json() == {'images': [image_base64], 'similar_images': True}

    response = api.health_assessment(image_path, custom_id=1)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == api.health_assessment_url
    assert request_record.json() == {'images': [image_base64], 'similar_images': True, 'custom_id': 1}


def test_get_health_assessment(api, api_key, health_assessment_dict, health_assessment, requests_mock):
    requests_mock.get(f'{api.identification_url}/{health_assessment_dict["access_token"]}', json=health_assessment_dict)
    response = api.get_health_assessment(health_assessment_dict['access_token'])
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.identification_url}/{health_assessment_dict["access_token"]}'
    assert request_record.headers['Api-Key'] == api_key
    assert response == health_assessment
    assert api.get_health_assessment(health_assessment_dict['access_token'], as_dict=True) == health_assessment_dict

    response = api.get_health_assessment(
        health_assessment_dict['access_token'],
        details=['treatment', 'local_name'],
        language='cz',
        full_disease_list=True,
    )
    request_record = requests_mock.request_history.pop()
    assert (
        request_record.url
        == f'{api.identification_url}/{health_assessment_dict["access_token"]}?details=treatment,local_name&language=cz&full_disease_list=true'
    )


def test_delete_health_assessment(api, api_key, health_assessment, requests_mock):
    requests_mock.delete(f'{api.identification_url}/{health_assessment.access_token}', json=True)
    response = api.delete_health_assessment(health_assessment.access_token)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'DELETE'
    assert request_record.url == f'{api.identification_url}/{health_assessment.access_token}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response

    response = api.delete_health_assessment(health_assessment)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{health_assessment.access_token}'

    health_assessment.custom_id = 123
    requests_mock.delete(f'{api.identification_url}/{health_assessment.custom_id}', json=True)
    response = api.delete_health_assessment(health_assessment.custom_id)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{health_assessment.custom_id}'


def test_delete_plant_identification(api, api_key, identification, requests_mock):
    identification.custom_id = 123
    requests_mock.delete(f'{api.identification_url}/{identification.custom_id}', json=True)
    response = api.delete_identification(identification.custom_id)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{identification.custom_id}'


def test_requests_to_plant_server(api: PlantApi, image_path):
    system_name = 'plant'
    run_test_requests_to_server(api, system_name, image_path, PlantIdentification)
    with staging_api(api, system_name) as api:
        custom_id = random.randint(1000000, 2000000)
        date_time = datetime.now()
        print(f'Health assessment asynchronous with {custom_id=} and {date_time=}:')
        health_assessment = api.health_assessment(
            image_path, asynchronous=True, custom_id=custom_id, date_time=date_time
        )
        print(health_assessment)
        print()

        print('Feedback for health assessment:')
        assert api.feedback(health_assessment.access_token, comment='correct', rating=5)

        health_assessment = api.get_health_assessment(
            health_assessment.access_token, full_disease_list=True, language='cz', details=['treatment']
        )
        print('Health assessment with treatment details, cz language and full_disease_list:')
        print(health_assessment)
        print()
        assert isinstance(health_assessment, HealthAssessment)
        assert 'treatment' in health_assessment.result.disease.suggestions[0].details
        assert health_assessment.result.disease.suggestions[0].details['language'] == 'cz'
        assert health_assessment.feedback.comment == 'correct'
        assert health_assessment.feedback.rating == 5
        assert health_assessment.custom_id == custom_id
        assert health_assessment.input.datetime == date_time

        print('Deleting health assessment:')
        assert api.delete_health_assessment(health_assessment.access_token)
        with pytest.raises(ValueError):
            api.get_health_assessment(health_assessment.access_token)
