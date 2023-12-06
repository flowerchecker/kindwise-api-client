import abc
import base64
import io
import json
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Any

import requests
from PIL import Image

from kindwise.models import Identification, UsageInfo


class KindwiseApi(abc.ABC):
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

    def feedback_url(self, token: str):
        return f'{self.identification_url}/{token}/feedback'

    def _make_api_call(self, url, method: str, data: dict | None = None):
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        return requests.request(method, url, json=data, headers=headers)

    def _encode_image(self, image: Path | str | bytes | BinaryIO, max_image_size: int | None) -> str:
        if isinstance(image, Path):  # Path
            with open(image, 'rb') as f:
                buffer = io.BytesIO(f.read())
        elif hasattr(image, 'read') and hasattr(image, 'seek') and hasattr(image, 'mode'):  # BinaryIO
            if 'rb' not in image.mode:  # what will it do if this if is not there
                raise ValueError(f'Invalid file mode {image.mode=}, expected "rb"(binary mode)')
            image.seek(0)
            buffer = io.BytesIO(image.read())
        else:  # str | bytes:

            def is_base64():
                try:
                    byte_image = image if isinstance(image, bytes) else image.encode('ascii')
                    return base64.b64encode(base64.b64decode(byte_image)) == byte_image
                except Exception:
                    return False

            if is_base64():
                buffer = io.BytesIO(base64.b64decode(image))
            else:
                sb_bytes = bytes(image, 'ascii') if isinstance(image, str) else image
                buffer = io.BytesIO(sb_bytes)

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
            resized_image.save(output_buffer, format='JPEG')
            resized_image_bytes = output_buffer.getvalue()
            output_buffer.close()
            return resized_image_bytes

        img = buffer.getvalue() if max_image_size is None else resize_image(buffer)
        buffer.close()
        return base64.b64encode(img).decode('ascii')

    def _build_payload(
        self,
        image: Path | str | list[str] | list[Path],
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
            payload.update(extra_post_params)
        return payload

    def identify(
        self,
        image: Path | str | bytes | BinaryIO | list[str | Path | bytes | BinaryIO],
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        as_dict: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        extra_get_params: str = None,
        extra_post_params: dict[str, Any] = None,
        **kwargs,
    ) -> Identification | dict:
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
        if not response.ok:
            raise ValueError(f'Error while creating an identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    def _build_query(
        self,
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        extra_get_params: str = None,
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
            if extra_get_params.startswith('?'):
                extra_get_params = extra_get_params[1:] + '&'
        async_query = f'async=true&' if asynchronous else ''
        query = f'?{details_query}{language_query}{async_query}{extra_get_params}'
        if query.endswith('&'):
            query = query[:-1]
        return '' if query == '?' else query

    def get_identification(
        self,
        token: str | int,
        details: str | list[str] = None,
        language: str | list[str] = None,
        extra_get_params: str = None,
        as_dict: bool = False,
    ) -> Identification | dict:
        query = self._build_query(details=details, language=language, extra_get_params=extra_get_params)
        url = f'{self.identification_url}/{token}{query}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting an identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    def delete_identification(self, identification: Identification | str | int) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        url = f'{self.identification_url}/{token}'
        response = self._make_api_call(url, 'DELETE')
        if not response.ok:
            raise ValueError(f'Error while deleting an identification: {response.status_code=} {response.text=}')
        return True

    def usage_info(self, as_dict: bool = False) -> UsageInfo | dict:
        response = self._make_api_call(self.usage_info_url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting an usage info: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else UsageInfo.from_dict(response.json())

    def feedback(
        self, identification: Identification | str | int, comment: str | None = None, rating: int | None = None
    ) -> bool:
        token = identification.access_token if isinstance(identification, Identification) else identification
        if comment is None and rating is None:
            raise ValueError('Either comment or rating must be provided')
        data = {}
        if comment is not None:
            data['comment'] = comment
        if rating is not None:
            data['rating'] = rating
        response = self._make_api_call(self.feedback_url(token), 'POST', data)
        if not response.ok:
            raise ValueError(f'Error while sending a feedback: {response.status_code=} {response.text=}')
        return True

    @property
    @abc.abstractmethod
    def views_path(self) -> Path:
        ...

    def available_details(self) -> list[dict[str, any]]:
        with open(self.views_path) as f:
            return json.load(f)
