from pathlib import Path

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import Identification, PlantIdentification, HealthAssessment


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
        image: Path | str | list[str] | list[Path],
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        health: bool = False,
    ):
        payload = super()._build_payload(
            image=image, similar_images=similar_images, latitude_longitude=latitude_longitude
        )
        if health:
            payload['health'] = 'all'
        return payload

    def identify(
        self,
        image: Path | str | list[str] | list[Path],
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        health: bool = False,
        as_dict: bool = False,
    ) -> PlantIdentification | dict:
        identification = super().identify(
            image=image,
            details=details,
            language=language,
            asynchronous=asynchronous,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            health=health,
            as_dict=True,
        )
        return identification if as_dict else PlantIdentification.from_dict(identification)

    def get_identification(
        self, token: str, details: str | list[str] = None, language: str | list[str] = None, as_dict: bool = False
    ) -> Identification:
        identification = super().get_identification(token=token, details=details, language=language, as_dict=True)
        return identification if as_dict else PlantIdentification.from_dict(identification)

    def _build_query(
        self,
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        full_disease_list: bool = False,
    ):
        query = super()._build_query(details, language, asynchronous)
        disease_query = f'full_disease_list=true' if full_disease_list else ''
        if disease_query == '':
            return query

        if query == '':
            return f'?{disease_query}'
        return f'{query}&{disease_query}'

    def health_assessment(
        self,
        image: Path | str | list[str] | list[Path],
        details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        full_disease_list: bool = False,
        as_dict: bool = False,
    ) -> HealthAssessment | dict:
        query = self._build_query(details, language, asynchronous, full_disease_list=full_disease_list)
        url = f'{self.health_assessment_url}{query}'
        payload = self._build_payload(image, similar_images=similar_images, latitude_longitude=latitude_longitude)
        response = self._make_api_call(url, 'POST', payload)
        if not response.ok:
            raise ValueError(f'Error while creating a health assessment: {response.status_code=} {response.text=}')
        health_assessment = response.json()
        return health_assessment if as_dict else HealthAssessment.from_dict(health_assessment)

    def get_health_assessment(
        self,
        token: str,
        details: str | list[str] = None,
        language: str | list[str] = None,
        full_disease_list: bool = False,
        as_dict: bool = False,
    ) -> HealthAssessment | dict:
        query = self._build_query(details=details, language=language, full_disease_list=full_disease_list)
        url = f'{self.identification_url}/{token}{query}'
        response = self._make_api_call(url, 'GET')
        if not response.ok:
            raise ValueError(f'Error while getting a health assessment: {response.status_code=} {response.text=}')
        health_assessment = response.json()
        return health_assessment if as_dict else HealthAssessment.from_dict(health_assessment)

    def delete_health_assessment(self, identification: HealthAssessment | str) -> bool:
        return self.delete_identification(identification)
