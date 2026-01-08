import enum
from pathlib import Path
from unittest.mock import patch
from kindwise.async_api.core import AsyncKindwiseApi
from kindwise.models import Identification
import pytest
import base64
import httpx


class TestKBType(str, enum.Enum):
    TEST = 'test'
    default = TEST


class AsyncTestApi(AsyncKindwiseApi[Identification, TestKBType]):
    default_kb_type = TestKBType.TEST

    @property
    def identification_url(self):
        return 'https://api.kindwise.com/api/v1/identification'

    @property
    def usage_info_url(self):
        return 'https://api.kindwise.com/api/v1/usage_info'

    @property
    def kb_api_url(self):
        return 'https://api.kindwise.com/api/v1/kb'

    @property
    def views_path(self):
        return Path('.')


@pytest.fixture
def api():
    return AsyncTestApi(api_key='test_key')


@pytest.fixture
def image_base64():
    return 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'


@pytest.fixture
def identification_data():
    return {
        'access_token': 'token',
        'model_version': 'test:1.0',
        'custom_id': None,
        'input': {
            'images': ['img'],
            'datetime': '2023-01-01T00:00:00',
            'latitude': None,
            'longitude': None,
            'similar_images': True,
        },
        'result': {'classification': {'suggestions': []}},
        'status': 'COMPLETED',
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'created': 1234567890,
        'completed': 1234567890,
    }


@pytest.mark.anyio
async def test_identify(api, respx_mock, identification_data, image_base64):
    respx_mock.post(api.identification_url).mock(return_value=httpx.Response(200, json=identification_data))

    # Pass bytes to avoid file path detection for short strings
    result = await api.identify(image_base64.encode('ascii'))
    assert isinstance(result, Identification)
    assert result.access_token == 'token'


@pytest.mark.anyio
async def test_get_identification(api, respx_mock, identification_data):
    respx_mock.get(f'{api.identification_url}/token').mock(return_value=httpx.Response(200, json=identification_data))

    result = await api.get_identification('token')
    assert isinstance(result, Identification)
    assert result.access_token == 'token'


@pytest.mark.anyio
async def test_identify_with_path(api, respx_mock, identification_data, image_base64):
    respx_mock.post(api.identification_url).mock(return_value=httpx.Response(200, json=identification_data))

    # Patch anyio.Path used in the async_core module
    with patch('kindwise.async_api.core.anyio.Path') as MockAnyioPath:
        mock_instance = MockAnyioPath.return_value

        real_bytes = base64.b64decode(image_base64)

        async def get_bytes():
            return real_bytes

        mock_instance.read_bytes.side_effect = get_bytes

        result = await api.identify('/tmp/fake.jpg')
        assert isinstance(result, Identification)
        assert result.access_token == 'token'


@pytest.mark.anyio
async def test_delete_identification(api, respx_mock):
    respx_mock.delete(f'{api.identification_url}/token').mock(return_value=httpx.Response(200, json=True))
    result = await api.delete_identification('token')
    assert result is True


@pytest.mark.anyio
async def test_usage_info(api, respx_mock):
    usage_data = {
        "active": True,
        "credit_limits": {"day": None, "week": None, "month": None, "total": 100},
        "used": {"day": 1, "week": 1, "month": 1, "total": 2},
        "can_use_credits": {"value": True, "reason": None},
        "remaining": {"day": None, "week": None, "month": None, "total": 98},
    }
    respx_mock.get(api.usage_info_url).mock(return_value=httpx.Response(200, json=usage_data))
    result = await api.usage_info()
    # It returns a UsageInfo object because as_dict=False by default
    assert result.active is True
    assert result.used.total == 2


@pytest.mark.anyio
async def test_feedback(api, respx_mock):
    respx_mock.post(f'{api.identification_url}/token/feedback').mock(return_value=httpx.Response(200, json=True))
    result = await api.feedback('token', rating=5)
    assert result is True


@pytest.mark.anyio
async def test_search(api, respx_mock):
    search_data = {
        'entities': [
            {
                'matched_in': 'Bee',
                'matched_in_type': 'common_name',
                'access_token': '1',
                'match_position': 0,
                'match_length': 3,
            }
        ],
        'entities_trimmed': False,
        'limit': 20,
    }
    respx_mock.get(f'{api.kb_api_url}/test/name_search').mock(return_value=httpx.Response(200, json=search_data))
    result = await api.search('Bee')
    assert len(result.entities) == 1
    assert result.entities[0].matched_in == 'Bee'


@pytest.mark.anyio
async def test_get_kb_detail(api, respx_mock):
    kb_data = {'gbif_id': 123}
    respx_mock.get(f'{api.kb_api_url}/test/token').mock(return_value=httpx.Response(200, json=kb_data))
    # get_kb_detail returns dict
    result = await api.get_kb_detail('token', details='gbif_id')
    assert result['gbif_id'] == 123


@pytest.mark.anyio
async def test_conversation_flow(api, respx_mock):
    # Ask question
    question_resp = {
        'messages': [{'content': 'hi', 'type': 'question', 'created': '2023-01-01T00:00:00'}],
        'identification': 'token',
        'remaining_calls': 10,
        'model_parameters': {},
        'feedback': {},
    }
    respx_mock.post(f'{api.identification_url}/token/conversation').mock(
        return_value=httpx.Response(200, json=question_resp)
    )

    conv = await api.ask_question('token', 'hi')
    assert conv.identification == 'token'
    assert len(conv.messages) == 1

    # Get conversation
    respx_mock.get(f'{api.identification_url}/token/conversation').mock(
        return_value=httpx.Response(200, json=question_resp)
    )
    conv_get = await api.get_conversation('token')
    assert conv_get.identification == 'token'

    # Conversation feedback
    respx_mock.post(f'{api.identification_url}/token/conversation/feedback').mock(
        return_value=httpx.Response(200, json=True)
    )
    res = await api.conversation_feedback('token', {'rating': 5})
    assert res is True

    # Delete conversation
    respx_mock.delete(f'{api.identification_url}/token/conversation').mock(return_value=httpx.Response(200, json=True))
    del_res = await api.delete_conversation('token')
    assert del_res is True
