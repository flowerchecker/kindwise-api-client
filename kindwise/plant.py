import json
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import PlantIdentification, HealthAssessment, ClassificationLevel, RawPlantIdentification


class PlantApi(KindwiseApi):
    host = 'https://plant.id'

    def __init__(self, api_key: str = None):
        api_key = settings.PLANT_API_KEY if api_key is None else api_key
        if api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "PLANT_API_KEY" key'
            )
        super().__init__(api_key)

    @property
    def identification_url(self):
        return f'{self.host}/api/v3/identification'

    @property
    def usage_info_url(self):
        return f'{self.host}/api/v3/usage_info'

    @property
    def health_assessment_url(self):
        return f'{self.host}/api/v3/health_assessment'

    def _build_payload(
        self,
        *args,
        health: bool = False,
        classification_level: str | ClassificationLevel = None,
        classification_raw: bool = False,
        **kwargs,
    ):
        payload = super()._build_payload(*args, **kwargs)
        if health:
            payload['health'] = 'all'
        if classification_level is not None:
            if not isinstance(classification_level, ClassificationLevel):
                classification_level = ClassificationLevel(classification_level)
            payload['classification_level'] = classification_level.value
        if classification_raw:
            payload['classification_raw'] = classification_raw
        return payload

    @staticmethod
    def _build_details(details: str | list[str] = None, disease_details: str | list[str] = None, health: bool = False):
        if isinstance(details, str):
            details = details.split(',')
        if disease_details is not None and health:
            disease_details = disease_details.split(',') if isinstance(disease_details, str) else disease_details
            details = [] if details is None else details
            details = list(dict.fromkeys(details + disease_details))
        return details

    def identify(
        self,
        image: Path | str | bytes | BinaryIO | list[str | Path | bytes | BinaryIO],
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        health: bool = False,
        classification_level: str | ClassificationLevel = None,
        classification_raw: bool = False,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        as_dict: bool = False,
        extra_get_params: str = None,
        extra_post_params: str = None,
    ) -> PlantIdentification | RawPlantIdentification | dict:
        identification = super().identify(
            image=image,
            details=self._build_details(details, disease_details, health),
            language=language,
            asynchronous=asynchronous,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            health=health,
            custom_id=custom_id,
            date_time=date_time,
            max_image_size=max_image_size,
            classification_level=classification_level,
            classification_raw=classification_raw,
            as_dict=True,
            extra_get_params=extra_get_params,
            extra_post_params=extra_post_params,
        )
        if as_dict:
            return identification
        if classification_raw:
            return RawPlantIdentification.from_dict(identification)
        return PlantIdentification.from_dict(identification)

    def get_identification(
        self,
        token: str | int,
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        as_dict: bool = False,
        extra_get_params: str = None,
    ) -> PlantIdentification | dict:
        identification = super().get_identification(
            token=token,
            details=self._build_details(details, disease_details, health=True),
            language=language,
            as_dict=True,
            extra_get_params=extra_get_params,
        )  # todo might be RawPlantIdentification
        return identification if as_dict else PlantIdentification.from_dict(identification)

    def _build_query(
        self,
        full_disease_list: bool = False,
        **kwargs,
    ):
        query = super()._build_query(**kwargs)
        disease_query = f'full_disease_list=true' if full_disease_list else ''
        if disease_query == '':
            return query

        if query == '':
            return f'?{disease_query}'
        return f'{query}&{disease_query}'

    def health_assessment(
        self,
        image: Path | str | bytes | BinaryIO | list[str | Path | bytes | BinaryIO],
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        full_disease_list: bool = False,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        as_dict: bool = False,
        extra_get_params: str = None,
        extra_post_params: str = None,
    ) -> HealthAssessment | dict:
        query = self._build_query(
            details=details,
            language=language,
            asynchronous=asynchronous,
            extra_get_params=extra_get_params,
            full_disease_list=full_disease_list,
        )
        url = f'{self.health_assessment_url}{query}'
        payload = self._build_payload(
            image,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            custom_id=custom_id,
            date_time=date_time,
            max_image_size=max_image_size,
            extra_post_params=extra_post_params,
        )
        response = self._make_api_call(url, 'POST', payload)
        if not response.ok:
            raise ValueError(f'Error while creating a health assessment: {response.status_code=} {response.text=}')
        health_assessment = response.json()
        return health_assessment if as_dict else HealthAssessment.from_dict(health_assessment)

    def get_health_assessment(
        self,
        token: str | int,
        details: str | list[str] = None,
        language: str | list[str] = None,
        full_disease_list: bool = False,
        as_dict: bool = False,
        extra_get_params: str = None,
    ) -> HealthAssessment | dict:
        query = self._build_query(
            details=details, language=language, full_disease_list=full_disease_list, extra_get_params=extra_get_params
        )
        url = f'{self.identification_url}/{token}{query}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting a health assessment: {response.status_code=} {response.text=}')
        health_assessment = response.json()
        return health_assessment if as_dict else HealthAssessment.from_dict(health_assessment)

    def delete_health_assessment(self, identification: HealthAssessment | str | int) -> bool:
        return self.delete_identification(identification)

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.plant.json'

    @classmethod
    def available_disease_details(cls) -> list[dict[str, any]]:
        with open(settings.APP_DIR / 'resources' / f'views.plant.disease.json') as f:
            return json.load(f)
