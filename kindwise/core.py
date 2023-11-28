import abc
import base64
from datetime import datetime
from pathlib import Path

import requests

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

    def _build_payload(
        self,
        image: Path | str | list[str] | list[Path],
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        **kwargs,
    ):
        if not isinstance(image, list):
            image = [image]

        def encode_file(file_name):
            with open(file_name, 'rb') as file:
                return base64.b64encode(file.read()).decode('ascii')

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
        image: Path | str | list[str] | list[Path],
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
        self, token: str, details: str | list[str] = None, language: str | list[str] = None, as_dict: bool = False
    ) -> Identification | dict:
        url = f'{self.identification_url}/{token}{self._build_query(details, language)}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting an identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    def delete_identification(self, identification: Identification | str) -> bool:
        token = identification if isinstance(identification, str) else identification.access_token
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

    def feedback(self, token: Identification | str, comment: str | None = None, rating: int | None = None) -> bool:
        token = token if isinstance(token, str) else token.access_token
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
