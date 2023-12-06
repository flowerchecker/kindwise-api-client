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
    IdentificationStatus,
    ClassificationLevel,
    RawPlantIdentification,
    RawPlantResult,
    RawClassification,
    TaxaSpecificSuggestion,
    PlantInput,
)
from .conftest import IMAGE_DIR, run_test_requests_to_server, staging_api, run_test_available_details
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
        input=PlantInput(
            images=['https://plant.id/media/imgs/87fd66a519c648deb8615c30fa734709.jpg'],
            datetime=datetime.fromisoformat('2023-11-28T08:38:48.538187+00:00'),
            latitude=None,
            longitude=None,
            similar_images=True,
            classification_level=None,
            classification_raw=False,
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
        status=IdentificationStatus('COMPLETED'),
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
def raw_identification() -> RawPlantIdentification:
    return RawPlantIdentification(
        access_token='xMafoSAC9lwuqFs',
        model_version='plant_id:3.4.1',
        custom_id=None,
        input=Input(
            images=['https://plant.id/media/imgs/3947041816fc4a8cb040f837e8774042.jpg'],
            datetime=datetime.fromisoformat('2023-12-06T11:48:45.941297+00:00'),
            latitude=49.2034,
            longitude=16.57318,
            similar_images=True,
        ),
        result=RawPlantResult(
            is_plant=ResultEvaluation(probability=1.0, binary=True, threshold=0.5),
            is_healthy=None,
            classification=RawClassification(
                suggestions=TaxaSpecificSuggestion(
                    genus=[
                        Suggestion(
                            id='f1e13ba892d06f23',
                            name='Aloe',
                            probability=0.99,
                            similar_images=[
                                SimilarImage(
                                    id='e59f28dadd4c4cb5f03f0f93865bddbc6ef17b92',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e59/f28dadd4c4cb5f03f0f93865bddbc6ef17b92.jpeg',
                                    similarity=0.73,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e59/f28dadd4c4cb5f03f0f93865bddbc6ef17b92.small.jpeg',
                                    license_name=None,
                                    license_url=None,
                                    citation=None,
                                ),
                                SimilarImage(
                                    id='c2d7e69290c189858185e9a91d9fb2e8126345b8',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c2d/7e69290c189858185e9a91d9fb2e8126345b8.jpg',
                                    similarity=0.66,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c2d/7e69290c189858185e9a91d9fb2e8126345b8.small.jpg',
                                    license_name=None,
                                    license_url=None,
                                    citation=None,
                                ),
                            ],
                            details={'language': 'en', 'entity_id': 'f1e13ba892d06f23'},
                        )
                    ],
                    species=[
                        Suggestion(
                            id='4ba05f1050481731',
                            name='Aloe vera',
                            probability=0.99,
                            similar_images=[
                                SimilarImage(
                                    id='ac89509bf07b85d202d9f53094eea6394ce354c4',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.jpeg',
                                    similarity=0.764,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/ac8/9509bf07b85d202d9f53094eea6394ce354c4.small.jpeg',
                                    license_name=None,
                                    license_url=None,
                                    citation=None,
                                ),
                                SimilarImage(
                                    id='d688b6a280e81d1a5b7bc2d0d2b8a1497f360551',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.jpeg',
                                    similarity=0.707,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/d68/8b6a280e81d1a5b7bc2d0d2b8a1497f360551.small.jpeg',
                                    license_name=None,
                                    license_url=None,
                                    citation=None,
                                ),
                            ],
                            details={'language': 'en', 'entity_id': '4ba05f1050481731'},
                        )
                    ],
                    infraspecies=[
                        Suggestion(
                            id='e196761efe72cbc8',
                            name='Gasteria carinata var. carinata',
                            probability=0.34154388,
                            similar_images=[
                                SimilarImage(
                                    id='c5b08b131915d6d36a6fbe1313c780e89510bcbf',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c5b/08b131915d6d36a6fbe1313c780e89510bcbf.jpeg',
                                    similarity=0.48,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c5b/08b131915d6d36a6fbe1313c780e89510bcbf.small.jpeg',
                                    license_name='CC BY-NC 4.0',
                                    license_url='https://creativecommons.org/licenses/by-nc/4.0/',
                                    citation='Adriaan Grobler',
                                ),
                                SimilarImage(
                                    id='e0a803ae9fa8a1d91d191521851ceddf36ee84c3',
                                    url='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e0a/803ae9fa8a1d91d191521851ceddf36ee84c3.jpeg',
                                    similarity=0.451,
                                    url_small='https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e0a/803ae9fa8a1d91d191521851ceddf36ee84c3.small.jpeg',
                                    license_name='CC BY-NC 4.0',
                                    license_url='https://creativecommons.org/licenses/by-nc/4.0/',
                                    citation='Stephan and Unelle Knoetze',
                                ),
                            ],
                            details={'language': 'en', 'entity_id': 'e196761efe72cbc8'},
                        )
                    ],
                )
            ),
            disease=None,
        ),
        status=IdentificationStatus.COMPLETED,
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1701863325.941297),
        completed=datetime.fromtimestamp(1701863326.55468),
        feedback=None,
    )


@pytest.fixture
def raw_identification_dict():
    return {
        'access_token': 'xMafoSAC9lwuqFs',
        'model_version': 'plant_id:3.4.1',
        'custom_id': None,
        'input': {
            'latitude': 49.2034,
            'longitude': 16.57318,
            'classification_level': 'all',
            'classification_raw': True,
            'similar_images': True,
            'images': ['https://plant.id/media/imgs/3947041816fc4a8cb040f837e8774042.jpg'],
            'datetime': '2023-12-06T11:48:45.941297+00:00',
        },
        'result': {
            'is_plant': {'probability': 1.0, 'binary': True, 'threshold': 0.5},
            'classification': {
                'suggestions': {
                    'species': [
                        {
                            'id': '4ba05f1050481731',
                            'name': 'Aloe vera',
                            'probability': 0.99,
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
                        }
                    ],
                    'genus': [
                        {
                            'id': 'f1e13ba892d06f23',
                            'name': 'Aloe',
                            'probability': 0.99,
                            'similar_images': [
                                {
                                    'id': 'e59f28dadd4c4cb5f03f0f93865bddbc6ef17b92',
                                    'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e59/f28dadd4c4cb5f03f0f93865bddbc6ef17b92.jpeg',
                                    'similarity': 0.73,
                                    'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e59/f28dadd4c4cb5f03f0f93865bddbc6ef17b92.small.jpeg',
                                },
                                {
                                    'id': 'c2d7e69290c189858185e9a91d9fb2e8126345b8',
                                    'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c2d/7e69290c189858185e9a91d9fb2e8126345b8.jpg',
                                    'similarity': 0.66,
                                    'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c2d/7e69290c189858185e9a91d9fb2e8126345b8.small.jpg',
                                },
                            ],
                            'details': {'language': 'en', 'entity_id': 'f1e13ba892d06f23'},
                        }
                    ],
                    'infraspecies': [
                        {
                            'id': 'e196761efe72cbc8',
                            'name': 'Gasteria carinata var. carinata',
                            'probability': 0.34154388,
                            'similar_images': [
                                {
                                    'id': 'c5b08b131915d6d36a6fbe1313c780e89510bcbf',
                                    'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c5b/08b131915d6d36a6fbe1313c780e89510bcbf.jpeg',
                                    'license_name': 'CC BY-NC 4.0',
                                    'license_url': 'https://creativecommons.org/licenses/by-nc/4.0/',
                                    'citation': 'Adriaan Grobler',
                                    'similarity': 0.48,
                                    'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/c5b/08b131915d6d36a6fbe1313c780e89510bcbf.small.jpeg',
                                },
                                {
                                    'id': 'e0a803ae9fa8a1d91d191521851ceddf36ee84c3',
                                    'url': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e0a/803ae9fa8a1d91d191521851ceddf36ee84c3.jpeg',
                                    'license_name': 'CC BY-NC 4.0',
                                    'license_url': 'https://creativecommons.org/licenses/by-nc/4.0/',
                                    'citation': 'Stephan and Unelle Knoetze',
                                    'similarity': 0.451,
                                    'url_small': 'https://plant-id.ams3.cdn.digitaloceanspaces.com/similar_images/3/e0a/803ae9fa8a1d91d191521851ceddf36ee84c3.small.jpeg',
                                },
                            ],
                            'details': {'language': 'en', 'entity_id': 'e196761efe72cbc8'},
                        }
                    ],
                }
            },
        },
        'status': 'COMPLETED',
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'created': 1701863325.941297,
        'completed': 1701863326.55468,
    }


@pytest.fixture
def image_path():
    return IMAGE_DIR / 'aloe-vera.jpg'


@pytest.fixture
def image_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def test_identify(
    api,
    api_key,
    identification,
    identification_dict,
    image_path,
    image_base64,
    request_matcher,
    raw_identification,
    raw_identification_dict,
):
    # check parsing
    request_matcher.check_identify_request(expected_result=identification)
    # check as_dict
    request_matcher.check_identify_request(expected_result=identification_dict, as_dict=True)
    # check health
    request_matcher.check_identify_request(expected_payload=[('health', 'all')], health=True)
    # check similar images
    request_matcher.check_identify_request(expected_payload=[('similar_images', False)], similar_images=False)
    request_matcher.check_identify_request(expected_payload=[('similar_images', True)])
    # check latitude_longitude
    request_matcher.check_identify_request(
        expected_payload=[('latitude', 1.0), ('longitude', 2.0)], latitude_longitude=(1.0, 2.0)
    )
    # check languages
    request_matcher.check_identify_request(expected_query='language=cz,de', language=['cz', 'de'])
    # check details
    request_matcher.check_identify_request(expected_query='details=image', details='image')
    # check async
    request_matcher.check_identify_request(expected_query='async=true', asynchronous=True)
    # check images
    request_matcher.check_identify_request(expected_payload=[('images', [image_base64])], max_image_size=None)
    request_matcher.check_identify_request(
        expected_payload=[('images', [image_base64, image_base64])],
        max_image_size=None,
        image=[image_path, image_path],
    )
    with open(image_path, 'rb') as f:
        request_matcher.check_identify_request(
            expected_payload=[('images', [image_base64])],
            max_image_size=None,
            image=f,
        )
    with open(image_path, 'rb') as f:
        request_matcher.check_identify_request(
            expected_payload=[('images', [image_base64])],
            max_image_size=None,
            image=f.read(),
        )
    # check custom_id
    request_matcher.check_identify_request(expected_payload=[('custom_id', 1)], custom_id=1)
    # check date_time
    date = '2023-11-28T08:38:48.538187+00:00'
    request_matcher.check_identify_request(expected_payload=[('datetime', date)], date_time=date)
    # check disease details
    request_matcher.check_identify_request(expected_query='details=image', disease_details='image', health=True)
    request_matcher.check_identify_request(
        expected_query='details=image', disease_details='image', details='image', health=True
    )
    request_matcher.check_identify_request(
        expected_query='details=image,treatment', disease_details='image,treatment', health=True
    )
    request_matcher.check_identify_request(
        expected_query='details=image,treatment', disease_details=['image', 'treatment'], health=True
    )
    request_matcher.check_identify_request(expected_query='', disease_details='image')
    # check classification_level
    request_matcher.check_identify_request(
        expected_payload=[('classification_level', 'all')], classification_level='all'
    )
    request_matcher.check_identify_request(
        expected_payload=[('classification_level', 'genus')], classification_level=ClassificationLevel.GENUS
    )
    request_matcher.check_identify_request(raises=ValueError, classification_level='non-existing')
    # check classification_raw
    request_matcher.check_identify_request(
        expected_payload=[('classification_raw', True)],
        output=raw_identification_dict,
        expected_result=raw_identification,
        classification_raw=True,
    )
    # check extra_post_params
    request_matcher.check_identify_request(expected_payload=[('test', 'test')], extra_post_params={'test': 'test'})
    # check extra_get_params
    request_matcher.check_identify_request(expected_query='test=test', extra_get_params='?test=test')


def test_get_identification(request_matcher):
    request_matcher.check_get_identification_request('details=image', details='image')
    request_matcher.check_get_identification_request(
        'details=image,treatment', details='image', disease_details='treatment'
    )
    # check extra_get_params
    request_matcher.check_get_identification_request(expected_query='test=test', extra_get_params='?test=test')


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
        status=IdentificationStatus.COMPLETED,
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
    api, api_key, image_path, image_base64, requests_mock, health_assessment_dict, health_assessment, request_matcher
):
    # check result
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_result=health_assessment, expected_payload=[('similar_images', True)]
    )
    # check full_disease_list
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_query='?full_disease_list=true', full_disease_list=True
    )
    # check language
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_query='?language=cz', language='cz'
    )
    # check details
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_query='?details=image', details='image'
    )
    # check custom_id
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_payload=[('custom_id', 1)], language='cz', custom_id=1
    )
    # check extra_post_params
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_payload=[('test', 'test')], extra_post_params={'test': 'test'}
    )
    # check extra_get_params
    request_matcher.check_health_assessment_request(
        health_assessment_dict, expected_query='test=test', extra_get_params='?test=test'
    )


def test_get_health_assessment(api, api_key, health_assessment_dict, health_assessment, requests_mock, request_matcher):
    # check result
    request_matcher.check_get_health_assessment_request(health_assessment_dict, expected_result=health_assessment)
    # check details
    request_matcher.check_get_health_assessment_request(
        health_assessment_dict, expected_query='details=image', details='image'
    )
    # check extra_get_params
    request_matcher.check_get_health_assessment_request(
        health_assessment_dict, expected_query='test=test', extra_get_params='?test=test'
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
            image_path,
            asynchronous=True,
            custom_id=custom_id,
            date_time=date_time,
            latitude_longitude=(49.20340, 16.57318),
            full_disease_list=True,
        )
        print(health_assessment)
        assert health_assessment.input.datetime == date_time
        assert health_assessment.input.similar_images
        assert health_assessment.input.latitude == 49.20340
        assert health_assessment.input.longitude == 16.57318
        assert health_assessment.custom_id == custom_id
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


def test_available_details(api):
    expected_view_names = {
        'common_names',
        'url',
        'description',
        'taxonomy',
        'rank',
        'name_authority',
        'gbif_id',
        'inaturalist_id',
        'image',
        'images',
        'synonyms',
        'edible_parts',
        'propagation_methods',
        'watering',
    }
    expected_license = {'description', 'image', 'images'}
    expected_localized = {'common_names', 'url', 'description'}

    run_test_available_details(expected_view_names, expected_license, expected_localized, api.available_details())


def test_available_disease_details(api):
    expected_view_names = {
        'local_name',
        'description',
        'url',
        'treatment',
        'classification',
        'common_names',
        'cause',
    }
    expected_license = set()
    expected_localized = {'local_name', 'description', 'url', 'common_names'}

    run_test_available_details(
        expected_view_names, expected_license, expected_localized, api.available_disease_details()
    )
