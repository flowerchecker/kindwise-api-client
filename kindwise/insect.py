import base64
from pathlib import Path

import requests

from kindwise import settings
from kindwise.models import Identification


class InsectApi:
    identify_url = 'https://insect.kindwise.com/api/v1/identification'

    def __init__(self, api_key: str = None):
        self._api_key = settings.API_KEY if api_key is None else api_key
        if self._api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "KINDWISE_API_KEY" key'
            )

    def identify(
        self,
        image: Path | str,
        details: list[str] = None,
        latitude_longitude: tuple[float, float] = None,
        language: str | list[str] = None,
        similar_images: bool = True,
        as_dict: bool = False,
    ) -> Identification:
        def encode_file(file_name):
            with open(file_name, "rb") as file:
                return base64.b64encode(file.read()).decode("ascii")

        params = {
            'images': [encode_file(image)],
            'similar_images': similar_images,
        }
        if latitude_longitude is not None:
            params["latitude"], params["longitude"] = latitude_longitude
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self._api_key,
        }
        url = f'{self.identify_url}{self.__build_query(details, language)}'
        response = requests.post(url, json=params, headers=headers)
        if not response.ok:
            raise ValueError(f'Error while creating identification: {response.status_code=} {response.text=}')
        data = response.json()
        return data if as_dict else Identification.from_dict(response.json())

    @staticmethod
    def __build_query(details: list[str] = None, language: str | list[str] = None):
        details_query = '' if details is None else f'details={",".join(details)}&'
        if isinstance(language, str):
            language = [language]
        language_query = '' if language is None else f'language={",".join(language)}'
        query = f'?{details_query}{language_query}'
        return '' if query == '?' else query
