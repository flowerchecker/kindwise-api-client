import abc
import base64
import enum
import io
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

import requests

from kindwise.models import Identification, UsageInfo


class InputType(str, enum.Enum):
    PATH = 'path'
    BASE64 = 'base64'
    STREAM = 'stream'
    FILE = 'file'


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

    def _build_payload(
        self,
        image: Path | str | list[str] | list[Path],
        input_type: InputType,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        **kwargs,
    ):
        if not isinstance(image, list):
            image = [image]

        def handle_base64_stream(file: str | bytes) -> str:
            try:
                sb_bytes = bytes(file, 'ascii') if isinstance(file, str) else file
                if base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes:
                    return sb_bytes.decode('ascii')
                raise ValueError('Invalid base64 stream')
            except Exception:
                raise ValueError('Invalid base64 stream')

        def handle_stream(file: str | bytes) -> str:
            sb_bytes = bytes(file, 'ascii') if isinstance(file, str) else file
            return base64.b64encode(sb_bytes).decode('ascii')

        def handle_path(file: str | Path) -> str:
            file = file if isinstance(file, Path) else Path(file)
            if not file.is_file():
                raise ValueError(f'File {file} does not exist')
            with open(file, 'rb') as file:
                return base64.b64encode(file.read()).decode('ascii')

        def handle_file_object(file: io.IOBase) -> str:
            if 'b' not in file.mode:
                raise ValueError('File must be opened in a binary mode')
            content = file.read()
            try:
                return base64.b64encode(content).decode('ascii')
            except (base64.binascii.Error, UnicodeDecodeError) as e:
                raise ValueError(f'Unable to decode {file=} to base64')

        def encode_file(file: str | bytes | Path | io.BytesIO) -> str:
            if input_type == InputType.PATH:
                if not isinstance(file, str) and not isinstance(file, Path):
                    raise ValueError(f'Invalid file type {type(file)=} for {input_type=}, expected str or Path')
                return handle_path(file)
            elif input_type == InputType.BASE64:
                if not isinstance(file, str) and not isinstance(file, bytes):
                    raise ValueError(f'Invalid file type {type(file)=} for {input_type=}, expected str or bytes')
                return handle_base64_stream(file)
            elif input_type == InputType.STREAM:
                if not isinstance(file, str) and not isinstance(file, bytes):
                    raise ValueError(f'Invalid file type {type(file)=} for {input_type=}, expected str or bytes')
                return handle_stream(file)
            elif input_type == InputType.FILE:
                if not isinstance(file, io.IOBase):
                    raise ValueError(f'Invalid file type {type(file)=} for {input_type=}, expected file object')
                return handle_file_object(file)
            else:
                raise ValueError(f'Invalid input type {input_type=}')

        payload = {
            'images': [encode_file(img) for img in image],
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
        return payload

    def identify(
        self,
        image: Path | str | bytes | BinaryIO | list[str | Path | bytes | BinaryIO],
        input_type: InputType = InputType.PATH,
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        as_dict: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        **kwargs,
    ) -> Identification | dict:
        payload = self._build_payload(
            image,
            input_type,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            custom_id=custom_id,
            date_time=date_time,
            **kwargs,
        )
        url = f'{self.identification_url}{self._build_query(details, language, asynchronous)}'
        response = self._make_api_call(url, 'POST', payload)
        if not response.ok:
            raise ValueError(f'Error while creating an identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    def _build_query(
        self, details: str | list[str] = None, language: str | list[str] = None, asynchronous: bool = False
    ):
        if isinstance(details, str):
            details = [details]
        details_query = '' if details is None else f'details={",".join(details)}&'
        if isinstance(language, str):
            language = [language]
        language_query = '' if language is None else f'language={",".join(language)}&'
        async_query = f'async=true&' if asynchronous else ''
        query = f'?{details_query}{language_query}{async_query}'
        if query.endswith('&'):
            query = query[:-1]
        return '' if query == '?' else query

    def get_identification(
        self, token: str | int, details: str | list[str] = None, language: str | list[str] = None, as_dict: bool = False
    ) -> Identification | dict:
        url = f'{self.identification_url}/{token}{self._build_query(details, language)}'
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
