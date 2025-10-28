import abc
import base64
import enum
import io
import json
from datetime import datetime
from pathlib import Path, PurePath
from typing import Any, BinaryIO, Generic, TypeVar

import requests
from PIL import Image

from kindwise.models import Conversation, Identification, SearchResult, UsageInfo

IdentificationType = TypeVar('IdentificationType')
KBType = TypeVar('KBType')


class KindwiseApi(abc.ABC, Generic[IdentificationType, KBType]):
    identification_class = Identification
    default_kb_type = None

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    @abc.abstractmethod
    def identification_url(self):
        ...

    @property
    @abc.abstractmethod
    def usage_info_url(self):
        ...

    @property
    @abc.abstractmethod
    def kb_api_url(self):
        ...

    def feedback_url(self, token: str):
        return f'{self.identification_url}/{token}/feedback'

    def conversation_url(self, token: str):
        return f'{self.identification_url}/{token}/conversation'

    def conversation_feedback_url(self, token: str):
        return f'{self.identification_url}/{token}/conversation/feedback'

    def _make_api_call(self, url, method: str, data: dict | None = None):
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        response = requests.request(method, url, json=data, headers=headers, timeout=60.0)
        if not response.ok:
            raise ValueError(f'Error while making an API call: {response.status_code=} {response.text=}')
        return response

    @staticmethod
    def _load_image_buffer(image: PurePath | str | bytes | BinaryIO | Image.Image) -> io.BytesIO:
        def get_from_url() -> None | bytes:
            if not isinstance(image, str) or not image.startswith(('http://', 'https://')):
                return None
            response = requests.get(image)
            if not response.ok:
                return None
            return io.BytesIO(response.content)

        if _img := get_from_url():
            return _img
        if isinstance(image, str) and len(image) <= 250:  # first try str as a path to a file
            image = Path(image)
        if isinstance(image, PurePath):  # Path
            with open(image, 'rb') as f:
                return io.BytesIO(f.read())
        if hasattr(image, 'read') and hasattr(image, 'seek') and hasattr(image, 'mode'):  # BinaryIO
            if 'rb' not in image.mode:  # what will it do if this is not there
                raise ValueError(f'Invalid file mode {image.mode=}, expected "rb"(binary mode)')
            image.seek(0)
            return io.BytesIO(image.read())
        if isinstance(image, Image.Image):
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG')
            return buffer
        # str | bytes:

        def is_base64():
            try:
                byte_image = image if isinstance(image, bytes) else image.encode('ascii')
                return base64.b64encode(base64.b64decode(byte_image)) == byte_image
            except Exception:
                return False

        if is_base64():
            return io.BytesIO(base64.b64decode(image))
        sb_bytes = bytes(image, 'ascii') if isinstance(image, str) else image
        return io.BytesIO(sb_bytes)

    @staticmethod
    def _encode_image(image: PurePath | str | bytes | BinaryIO | Image.Image, max_image_size: int | None) -> str:
        buffer = KindwiseApi._load_image_buffer(image)

        def resize_image(file) -> bytes:
            img = Image.open(file)
            if max(img.size) <= max_image_size:
                resized_image = img
            else:
                aspect_ratio = img.width / img.height
                new_width = max_image_size if aspect_ratio >= 1 else int(max_image_size * aspect_ratio)
                new_height = int(new_width / aspect_ratio)
                resized_image = img.resize((new_width, new_height))
            output_buffer = io.BytesIO()
            if resized_image.mode != 'RGB':
                resized_image = resized_image.convert('RGB')
            resized_image.save(output_buffer, format='JPEG')
            resized_image_bytes = output_buffer.getvalue()
            output_buffer.close()
            return resized_image_bytes

        img = buffer.getvalue() if max_image_size is None else resize_image(buffer)
        buffer.close()
        return base64.b64encode(img).decode('ascii')

    def _build_payload(
        self,
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        extra_post_params: dict[str, Any] = None,
        **kwargs,
    ):
        if not isinstance(image, list):
            image = [image]

        payload = {
            'images': [self._encode_image(img, max_image_size) for img in image],
            'similar_images': similar_images,
        }
        if latitude_longitude is not None:
            payload['latitude'], payload['longitude'] = latitude_longitude
        if custom_id is not None:
            payload['custom_id'] = custom_id
        if date_time is not None:
            if isinstance(date_time, datetime):
                payload['datetime'] = date_time.isoformat()
            elif isinstance(date_time, str):
                # check if ISO format is valid
                payload['datetime'] = datetime.fromisoformat(date_time).isoformat()
            elif isinstance(date_time, float):
                payload['datetime'] = datetime.fromtimestamp(date_time).isoformat()
            else:
                raise ValueError(f'Invalid date_time format {date_time=} {type(date_time)=}')
        if extra_post_params is not None:
            if 'suggestion_filter' in extra_post_params and isinstance(extra_post_params['suggestion_filter'], str):
                extra_post_params['suggestion_filter'] = {'classification': extra_post_params['suggestion_filter']}
            payload.update(extra_post_params)
        return payload

    def identify(
        self,
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        as_dict: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        extra_get_params: str | dict[str | Any] = None,
        extra_post_params: dict[str, Any] = None,
        **kwargs,
    ) -> IdentificationType | dict:
        payload = self._build_payload(
            image,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            custom_id=custom_id,
            date_time=date_time,
            max_image_size=max_image_size,
            extra_post_params=extra_post_params,
            **kwargs,
        )
        query = self._build_query(
            details=details, language=language, asynchronous=asynchronous, extra_get_params=extra_get_params, **kwargs
        )
        url = f'{self.identification_url}{query}'
        response = self._make_api_call(url, 'POST', payload)
        data = response.json()
        return data if as_dict else self.identification_class.from_dict(data)

    def _build_query(
        self,
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        extra_get_params: str | dict[str, str] = None,
        limit: int = None,
        query: str = None,
        **kwargs,
    ):
        if isinstance(details, str):
            details = [details]
        details_query = '' if details is None else f'details={",".join(details)}&'
        if isinstance(language, str):
            language = [language]
        language_query = '' if language is None else f'language={",".join(language)}&'
        if extra_get_params is None:
            extra_get_params = ''
        else:
            if isinstance(extra_get_params, dict):
                extra_get_params = '&'.join(f'{k}={v}' for k, v in extra_get_params.items())
            if extra_get_params.startswith('?'):
                extra_get_params = extra_get_params[1:] + '&'
        async_query = f'async=true&' if asynchronous else ''
        query = '' if query is None else f'q={query}&'
        limit = '' if limit is None else f'limit={limit}&'
        query = f'?{query}{limit}{details_query}{language_query}{async_query}{extra_get_params}'
        if query.endswith('&'):
            query = query[:-1]
        return '' if query == '?' else query

    def get_identification(
        self,
        token: str | int,
        details: str | list[str] = None,
        language: str | list[str] = None,
        extra_get_params: str | dict[str, str] = None,
        as_dict: bool = False,
    ) -> IdentificationType | dict:
        query = self._build_query(details=details, language=language, extra_get_params=extra_get_params)
        url = f'{self.identification_url}/{token}{query}'
        response = self._make_api_call(url, 'GET')
        data = response.json()
        return data if as_dict else self.identification_class.from_dict(data)

    def delete_identification(self, identification: IdentificationType | str | int) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        url = f'{self.identification_url}/{token}'
        self._make_api_call(url, 'DELETE')
        return True

    def usage_info(self, as_dict: bool = False) -> UsageInfo | dict:
        response = self._make_api_call(self.usage_info_url, 'GET')
        data = response.json()
        return data if as_dict else UsageInfo.from_dict(data)

    def feedback(
        self, identification: IdentificationType | str | int, comment: str | None = None, rating: int | None = None
    ) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        if comment is None and rating is None:
            raise ValueError('Either comment or rating must be provided')
        data = {}
        if comment is not None:
            data['comment'] = comment
        if rating is not None:
            data['rating'] = rating
        self._make_api_call(self.feedback_url(token), 'POST', data)
        return True

    @property
    @abc.abstractmethod
    def views_path(self) -> Path:
        ...

    def available_details(self) -> list[dict[str, any]]:
        with open(self.views_path) as f:
            return json.load(f)

    def search(
        self,
        query: str,
        limit: int = None,
        language: str = None,
        kb_type: KBType | str = None,
        as_dict=False,
    ) -> SearchResult | dict:
        if not query:
            raise ValueError('Query parameter q must be provided')
        if isinstance(limit, int) and limit < 1:
            raise ValueError(f'Limit must be positive integer.')
        if kb_type is None:
            kb_type = self.default_kb_type
        if isinstance(kb_type, enum.Enum):
            kb_type = kb_type.value
        url = f'{self.kb_api_url}/{kb_type}/name_search{self._build_query(query=query, limit=limit, language=language)}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while searching knowledge base: {response.status_code=} {response.text=}')
        return response.json() if as_dict else SearchResult.from_dict(response.json())

    def get_kb_detail(
        self, access_token: str, details: str | list[str], language: str = None, kb_type: KBType | str = None
    ) -> dict:
        if kb_type is None:
            kb_type = self.default_kb_type
        if isinstance(kb_type, enum.Enum):
            kb_type = kb_type.value
        url = f'{self.kb_api_url}/{kb_type}/{access_token}{self._build_query(language=language, details=details)}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting knowledge base detail: {response.status_code=} {response.text=}')
        return response.json()

    def ask_question(
        self,
        identification: IdentificationType | str | int,
        question: str,
        model: str = None,
        app_name: str = None,
        prompt: str = None,
        temperature: float = None,
        as_dict: bool = False,
    ) -> Conversation:
        token = identification.access_token if isinstance(identification, Identification) else identification
        data = {'question': question}
        for key, value in [('model', model), ('app_name', app_name), ('prompt', prompt), ('temperature', temperature)]:
            if value is not None:
                data[key] = value
        response = self._make_api_call(self.conversation_url(token), 'POST', data)
        data = response.json()
        return data if as_dict else Conversation.from_dict(data)

    def get_conversation(self, identification: IdentificationType | str | int) -> Conversation:
        token = identification.access_token if isinstance(identification, Identification) else identification
        response = self._make_api_call(self.conversation_url(token), 'GET')
        return Conversation.from_dict(response.json())

    def delete_conversation(self, identification: IdentificationType | str | int) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        self._make_api_call(self.conversation_url(token), 'DELETE')
        return True

    def conversation_feedback(self, identification: IdentificationType | str | int, feedback: str | int | dict) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        self._make_api_call(self.conversation_feedback_url(token), 'POST', {'feedback': feedback})
        return True
