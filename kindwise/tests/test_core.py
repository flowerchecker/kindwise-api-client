import base64
import io
from datetime import datetime

import pytest
from PIL import Image

from kindwise.insect import InsectApi
from kindwise.models import (
    Identification,
    Result,
    Input,
    Classification,
    Suggestion,
    SimilarImage,
    IdentificationStatus,
)
from .conftest import IMAGE_DIR


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
def image_base64(image_path):
    with open(image_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('ascii')


def test_identify(
    api, api_key, identification, identification_dict, image_path, image_base64, requests_mock, request_matcher
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
