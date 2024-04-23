import base64
import enum
import io
from datetime import datetime
from pathlib import PurePath, Path

import pytest
from PIL import Image

from kindwise.models import (
    Identification,
    Result,
    Input,
    Classification,
    Suggestion,
    SimilarImage,
    IdentificationStatus,
    SearchResult,
    SearchEntity,
)
from .conftest import IMAGE_DIR
from .. import settings
from ..core import KindwiseApi


class TestKBType(str, enum.Enum):
    TEST = 'test'
    TEST_2 = 'test_2'
    default = TEST


class TestApi(KindwiseApi[Identification, TestKBType]):
    host = 'http://test.id'
    default_kb_type = TestKBType.TEST

    @property
    def identification_url(self):
        return f'{self.host}/api/v1/identification'

    @property
    def usage_info_url(self):
        return f'{self.host}/api/v1/usage_info'

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.insect.json'

    @property
    def kb_api_url(self):
        return f'{self.host}/api/v1/kb'


@pytest.fixture
def api(api_key):
    api_ = TestApi(api_key=api_key)
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
        status=IdentificationStatus.COMPLETED,
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1700642966.136448),
        completed=datetime.fromtimestamp(1700642966.580449),
        feedback=None,
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
def image(image_path):
    with open(image_path, 'rb') as file:
        return file.read()


@pytest.fixture
def image_base64(image):
    return base64.b64encode(image).decode('ascii')


def test_identify(
    api, api_key, identification, identification_dict, image_path, image, image_base64, requests_mock, request_matcher
):
    # check result
    request_matcher.check_identify_request(expected_result=identification, max_image_size=None)
    # check as_dict
    request_matcher.check_identify_request(expected_result=identification_dict, max_image_size=None, as_dict=True)
    # check similar images
    request_matcher.check_identify_request(expected_payload=[('similar_images', False)], similar_images=False)
    request_matcher.check_identify_request(expected_payload=[('similar_images', True)])
    # check latitude_longitude
    request_matcher.check_identify_request(
        expected_payload=[('latitude', 1.0), ('longitude', 2.0)], latitude_longitude=(1.0, 2.0)
    )
    # check languages
    request_matcher.check_identify_request(expected_query='language=cz,de', language=['cz', 'de'])
    request_matcher.check_identify_request(expected_query='language=cz', language='cz')
    request_matcher.check_identify_request(expected_query='language=cz,de', language='cz,de')
    # check details
    request_matcher.check_identify_request(expected_query='details=image', details='image')
    request_matcher.check_identify_request(expected_query='details=image,treatment', details=['image', 'treatment'])
    request_matcher.check_identify_request(expected_query='details=image,treatment', details='image,treatment')
    # check async
    request_matcher.check_identify_request(expected_query='async=true', asynchronous=True)
    # check custom_id
    request_matcher.check_identify_request(expected_payload=[('custom_id', 1)], custom_id=1)
    # check date_time
    date = '2023-11-28T08:38:48.538187'
    request_matcher.check_identify_request(expected_payload=[('datetime', date)], date_time=date)
    request_matcher.check_identify_request(
        expected_payload=[('datetime', date)], date_time=datetime.fromisoformat(date)
    )
    request_matcher.check_identify_request(
        expected_payload=[('datetime', date)], date_time=datetime.fromisoformat(date).timestamp()
    )
    request_matcher.check_identify_request(
        expected_payload=[('datetime', date)], raises=ValueError, date_time='2023-20-20'
    )
    # check input image
    request_matcher.check_identify_request(
        expected_payload=[('images', [image_base64, image_base64])],
        max_image_size=None,
        image=[image_path, image_path],
    )
    # accept image as a str path to a file
    request_matcher.check_identify_request(
        expected_payload=[('images', [image_base64])],
        max_image_size=None,
        image=[str(image_path)],
    )
    # accept image as base64 string
    request_matcher.check_identify_request(
        expected_payload=[('images', [image_base64])], max_image_size=None, image=image_base64
    )
    # accept image as base64 bytes
    request_matcher.check_identify_request(
        expected_payload=[('images', [image_base64])], max_image_size=None, image=image_base64.encode('ascii')
    )
    # accept image as a file object
    with open(image_path, 'rb') as f:
        request_matcher.check_identify_request(
            expected_payload=[('images', [image_base64])], max_image_size=None, image=f
        )
    # accept image as a byte stream
    with open(image_path, 'rb') as f:
        request_matcher.check_identify_request(
            expected_payload=[('images', [image_base64])], max_image_size=None, image=f.read()
        )
    # accept image as a PurePath and accept png format
    pure_path = PurePath(settings.APP_DIR) / 'tests' / 'resources' / 'images' / 'padli.png'
    pure_path_base64 = api._encode_image(pure_path, 1500)
    request_matcher.check_identify_request(expected_payload=[('images', [pure_path_base64])], image=pure_path)
    # accept image as a PIL image
    # with open(image_path, 'rb') as f:
    img = Image.open(image_path)
    request_matcher.check_identify_request(image=img, max_image_size=None)
    # accept image as url
    requests_mock.get('http://example.com/image.jpg', content=image)
    request_matcher.check_identify_request(
        image='http://example.com/image.jpg', max_image_size=None, expected_payload=[('images', [image_base64])]
    )

    # check if image is resized
    with open(image_path, 'rb') as f:
        img = Image.open(f)
        max_size = max(img.size)
        new_size = max_size - 100

    def run_test_resize(img):
        api.identify(img, max_image_size=new_size)
        request_record = requests_mock.request_history.pop()
        send_img = request_record.json()['images'][0]
        decoded = base64.b64decode(send_img)
        send_img = Image.open(io.BytesIO(decoded))
        assert max(send_img.size) == new_size

    run_test_resize(image_path)
    run_test_resize(image_base64)
    with open(image_path, 'rb') as f:
        run_test_resize(f)
    with open(image_path, 'rb') as f:
        run_test_resize(f.read())
    # check extra_post_params
    request_matcher.check_identify_request(expected_payload=[('test', 'test')], extra_post_params={'test': 'test'})
    # check extra_get_params
    request_matcher.check_identify_request(expected_query='test=test', extra_get_params='?test=test')
    request_matcher.check_identify_request(expected_query='test=test', extra_get_params='test=test')
    request_matcher.check_identify_request(expected_query='test=test', extra_get_params='test=test&')
    request_matcher.check_identify_request(
        expected_query='details=image&test=test', details=['image'], extra_get_params='?test=test'
    )
    request_matcher.check_identify_request(
        expected_query='details=image&test=test', details=['image'], extra_get_params='test=test'
    )
    request_matcher.check_identify_request(
        expected_query='details=image&test=test', details=['image'], extra_get_params='test=test&'
    )
    request_matcher.check_identify_request(expected_query='test=test', extra_get_params={'test': 'test'})
    request_matcher.check_identify_request(expected_query='', extra_get_params={})


def test_get_identification(
    api, api_key, identification, identification_dict, image_path, requests_mock, request_matcher
):
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
    # check extra_get_params
    request_matcher.check_get_identification_request(expected_query='test=test', extra_get_params='?test=test')
    request_matcher.check_get_identification_request(expected_query='test=test', extra_get_params={'test': 'test'})


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

    response = api.delete_identification(identification)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.identification_url}/{identification.access_token}'


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

    response = api.feedback(identification, comment='correct')
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identification_url}/{identification.access_token}/feedback'


def test_search(api, api_key, requests_mock):
    requests_mock.get(
        f'{api.kb_api_url}/{TestKBType.TEST}/name_search',
        json={
            'entities': [
                {
                    'matched_in': 'Bee Beetle',
                    'matched_in_type': 'common_name',
                    'access_token': 'VW5rUkREcXFEVFM2SzM2dDYKXDBzJ0lIJzVjUy8LDk0-',
                    'match_position': 0,
                    'match_length': 3,
                },
            ],
            'entities_trimmed': False,
            'limit': 20,
        },
    )
    response = api.search('bee')
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/name_search?q=bee'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response == SearchResult(
        entities=[
            SearchEntity('Bee Beetle', 'common_name', 'VW5rUkREcXFEVFM2SzM2dDYKXDBzJ0lIJzVjUy8LDk0-', 0, 3),
        ],
        entities_trimmed=False,
        limit=20,
    )
    api.search('vcela', language='cz', limit=1)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/name_search?q=vcela&limit=1&language=cz'
    # check bundle
    api = TestApi(api_key=api_key)
    plant_api_res = {
        'entities': [
            {
                'matched_in': 'Aloe',
                'matched_in_type': 'entity_name',
                'access_token': 'bG1NbjFDTkoxOHNTTHlIYwpcKF8CIS9yCAoXY3ofelA-',
                'match_position': 0,
                'match_length': 4,
            }
        ],
        'entities_trimmed': True,
        'limit': 20,
    }
    requests_mock.get(f'{api.kb_api_url}/{TestKBType.TEST}/name_search', json=plant_api_res)
    api.search('aloe')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/name_search?q=aloe'
    requests_mock.get(f'{api.kb_api_url}/{TestKBType.TEST_2}/name_search', json=plant_api_res)
    api.search('downy', kb_type=TestKBType.TEST_2)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST_2}/name_search?q=downy'
    with pytest.raises(ValueError):
        api.search('downy', limit=0)


def test_get_kb_detail(api, api_key, requests_mock):
    access_token = 's34d5rft6gyu'
    requests_mock.get(
        f'{api.kb_api_url}/{TestKBType.TEST}/{access_token}',
        json={'gbif_id': 1085281, 'rank': 'species', 'language': 'en', 'name': 'Trichius gallicus'},
    )
    response = api.get_kb_detail(access_token, 'rank,gbif_id')
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'GET'
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/{access_token}?details=rank,gbif_id'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert response == {'gbif_id': 1085281, 'rank': 'species', 'language': 'en', 'name': 'Trichius gallicus'}

    api.get_kb_detail(access_token, ['rank', 'gbif_id'], language='cs')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/{access_token}?details=rank,gbif_id&language=cs'

    # check bundle
    api = TestApi(api_key=api_key)
    requests_mock.get(
        f'{api.kb_api_url}/{TestKBType.TEST}/{access_token}',
        json={'gbif_id': 2777724, 'rank': 'species', 'language': 'en', 'name': 'Aloe vera'},
    )
    response = api.get_kb_detail(access_token, 'rank,gbif_id')
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST}/{access_token}?details=rank,gbif_id'
    assert response == {'gbif_id': 2777724, 'rank': 'species', 'language': 'en', 'name': 'Aloe vera'}

    requests_mock.get(
        f'{api.kb_api_url}/{TestKBType.TEST_2}/{access_token}',
        json={'url': 'https://en.wikipedia.org/wiki/Downy_mildew', 'language': 'en', 'name': 'downy mildew'},
    )
    response = api.get_kb_detail(access_token, 'url', kb_type=TestKBType.TEST_2)
    request_record = requests_mock.request_history.pop()
    assert request_record.url == f'{api.kb_api_url}/{TestKBType.TEST_2}/{access_token}?details=url'
    assert response == {'url': 'https://en.wikipedia.org/wiki/Downy_mildew', 'language': 'en', 'name': 'downy mildew'}
