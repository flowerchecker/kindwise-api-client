import base64
from pathlib import Path

import requests

from kindwise import settings
from kindwise.models import Identification, UsageInfo


class InsectApi:
    host = 'https://insect.kindwise.com'

    def __init__(self, api_key: str = None):
        self.api_key = settings.INSECT_API_KEY if api_key is None else api_key
        if self.api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "INSECT_API_KEY" key'
            )

    @property
    def identification_url(self):
        return f'{self.host}/api/v1/identification'

    @property
    def usage_info_url(self):
        return f'{self.host}/api/v1/usage_info'

    def feedback_url(self, token: str):
        return f'{self.identification_url}/{token}/feedback'

    def identify(
        self,
        image: Path | str | list[str] | list[Path],
        details: str | list[str] = None,
        latitude_longitude: tuple[float, float] = None,
        language: str | list[str] = None,
        similar_images: bool = True,
        asynchronous: bool = False,
        as_dict: bool = False,
    ) -> Identification:
        def encode_file(file_name):
            with open(file_name, "rb") as file:
                return base64.b64encode(file.read()).decode("ascii")

        if not isinstance(image, list):
            image = [image]

        params = {
            'images': [encode_file(img) for img in image],
            'similar_images': similar_images,
        }
        if latitude_longitude is not None:
            params["latitude"], params["longitude"] = latitude_longitude
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }
        url = f'{self.identification_url}{self.__build_query(details, language, asynchronous)}'
        response = requests.post(url, json=params, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while creating identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    @staticmethod
    def __build_query(details: str | list[str] = None, language: str | list[str] = None, asynchronous: bool = False):
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
    ) -> Identification:
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        url = f'{self.identification_url}/{token}{self.__build_query(details, language)}'
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while getting identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    def delete_identification(self, token: str) -> bool:
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        url = f'{self.identification_url}/{token}'
        response = requests.delete(url, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while deleting identification: {response.status_code=} {response.text=}')
        return True

    def usage_info(self, as_dict: bool = False) -> UsageInfo | dict:
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        response = requests.get(self.usage_info_url, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while getting usage info: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else UsageInfo.from_dict(response.json())

    def feedback(self, token: str, comment: str | None = None, rating: int | None = None) -> bool:
        if comment is None and rating is None:
            raise ValueError('Either comment or rating must be provided')
        headers = {
            'Content-Type': 'application/json',
            'Api-Key': self.api_key,
        }
        url = self.feedback_url(token)
        data = {}
        if comment is not None:
            data['comment'] = comment
        if rating is not None:
            data['rating'] = rating
        response = requests.post(url, json=data, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while sending feedback: {response.status_code=} {response.text=}')
        return True
