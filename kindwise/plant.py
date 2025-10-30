import enum
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePath
from typing import BinaryIO

from PIL import Image

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import (
    ClassificationLevel,
    Identification,
    Input,
    IdentificationStatus,
    Feedback,
    ResultEvaluation,
    Classification,
    Suggestion,
)


class PlantKBType(str, enum.Enum):
    PLANTS = 'plants'
    DISEASES = 'diseases'


@dataclass
class PlantResult:
    is_plant: ResultEvaluation
    is_healthy: ResultEvaluation | None
    classification: Classification
    disease: Classification | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_plant=ResultEvaluation.from_dict(data['is_plant']),
            is_healthy=ResultEvaluation.from_dict(data['is_healthy']) if 'is_healthy' in data else None,
            classification=Classification.from_dict(data['classification']),
            disease=Classification.from_dict(data['disease']) if 'disease' in data else None,
        )


@dataclass
class PlantInput(Input):
    classification_level: ClassificationLevel | None
    classification_raw: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'PlantInput':
        return cls(
            images=data['images'],
            datetime=datetime.fromisoformat(data['datetime']),
            latitude=data['latitude'],
            longitude=data['longitude'],
            similar_images=data['similar_images'],
            classification_level=ClassificationLevel(data['classification_level'])
            if 'classification_level' in data
            else None,
            classification_raw=data.get('classification_raw', False),
        )


@dataclass
class PlantIdentification(Identification):
    result: PlantResult | None
    input: PlantInput

    @classmethod
    def from_dict(cls, data: dict) -> 'PlantIdentification':
        return cls(
            access_token=data['access_token'],
            model_version=data['model_version'],
            custom_id=data['custom_id'],
            input=PlantInput.from_dict(data['input']),
            result=None if 'result' not in data else PlantResult.from_dict(data['result']),
            status=IdentificationStatus(data['status']),
            sla_compliant_client=data['sla_compliant_client'],
            sla_compliant_system=data['sla_compliant_system'],
            created=datetime.fromtimestamp(data['created']),
            completed=None if data['completed'] is None else datetime.fromtimestamp(data['completed']),
            feedback=Feedback.from_dict(data['feedback']) if 'feedback' in data else None,
        )


@dataclass
class TaxaSpecificSuggestion:
    genus: list[Suggestion]
    species: list[Suggestion]
    infraspecies: list[Suggestion] | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            genus=[Suggestion.from_dict(suggestion) for suggestion in data['genus']],
            species=[Suggestion.from_dict(suggestion) for suggestion in data['species']],
            infraspecies=None
            if 'infraspecies' not in data
            else [Suggestion.from_dict(suggestion) for suggestion in data['infraspecies']],
        )


@dataclass
class RawClassification:
    suggestions: TaxaSpecificSuggestion

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            suggestions=TaxaSpecificSuggestion.from_dict(data['suggestions']),
        )


@dataclass
class RawPlantResult:
    is_plant: ResultEvaluation
    is_healthy: ResultEvaluation | None
    classification: RawClassification
    disease: Classification | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_plant=ResultEvaluation.from_dict(data['is_plant']),
            is_healthy=ResultEvaluation.from_dict(data['is_healthy']) if 'is_healthy' in data else None,
            classification=RawClassification.from_dict(data['classification']),
            disease=Classification.from_dict(data['disease']) if 'disease' in data else None,
        )


@dataclass
class RawPlantIdentification(Identification):
    result: RawPlantResult | None

    @classmethod
    def from_dict(cls, data: dict) -> 'RawPlantIdentification':
        return cls(
            access_token=data['access_token'],
            model_version=data['model_version'],
            custom_id=data['custom_id'],
            input=Input.from_dict(data['input']),
            result=None if 'result' not in data else RawPlantResult.from_dict(data['result']),
            status=IdentificationStatus(data['status']),
            sla_compliant_client=data['sla_compliant_client'],
            sla_compliant_system=data['sla_compliant_system'],
            created=datetime.fromtimestamp(data['created']),
            completed=None if data['completed'] is None else datetime.fromtimestamp(data['completed']),
            feedback=Feedback.from_dict(data['feedback']) if 'feedback' in data else None,
        )


@dataclass
class HealthAssessmentResult:
    is_plant: ResultEvaluation
    is_healthy: ResultEvaluation
    disease: Classification

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_plant=ResultEvaluation.from_dict(data['is_plant']),
            is_healthy=ResultEvaluation.from_dict(data['is_healthy']),
            disease=Classification.from_dict(data['disease']),
        )


@dataclass
class HealthAssessment(Identification):
    result: HealthAssessmentResult | None

    @classmethod
    def from_dict(cls, data: dict) -> 'HealthAssessment':
        return cls(
            access_token=data['access_token'],
            model_version=data['model_version'],
            custom_id=data['custom_id'],
            input=Input.from_dict(data['input']),
            result=None if 'result' not in data else HealthAssessmentResult.from_dict(data['result']),
            status=data['status'],
            sla_compliant_client=data['sla_compliant_client'],
            sla_compliant_system=data['sla_compliant_system'],
            created=datetime.fromtimestamp(data['created']),
            completed=None if data['completed'] is None else datetime.fromtimestamp(data['completed']),
            feedback=Feedback.from_dict(data['feedback']) if 'feedback' in data else None,
        )


class PlantApi(KindwiseApi[PlantIdentification, PlantKBType]):
    host = 'https://plant.id'
    default_kb_type = PlantKBType.PLANTS

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
    def kb_api_url(self):
        return f'{self.host}/api/v3/kb'

    @property
    def health_assessment_url(self):
        return f'{self.host}/api/v3/health_assessment'

    def _build_payload(
        self,
        *args,
        health: str = None,
        classification_level: str | ClassificationLevel = None,
        classification_raw: bool = False,
        **kwargs,
    ):
        payload = super()._build_payload(*args, **kwargs)
        if health is not None:
            payload['health'] = health
        if classification_level is not None:
            if not isinstance(classification_level, ClassificationLevel):
                classification_level = ClassificationLevel(classification_level)
            payload['classification_level'] = classification_level.value
        if classification_raw:
            payload['classification_raw'] = classification_raw
        return payload

    @staticmethod
    def _build_details(details: str | list[str] = None, disease_details: str | list[str] = None):
        if isinstance(details, str):
            details = details.split(',')
        if disease_details is not None:
            disease_details = disease_details.split(',') if isinstance(disease_details, str) else disease_details
            details = [] if details is None else details
            details = list(dict.fromkeys(details + disease_details))
        return details

    def identify(
        self,
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        health: str = None,
        classification_level: str | ClassificationLevel = None,
        classification_raw: bool = False,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        as_dict: bool = False,
        extra_get_params: str | dict[str, str] = None,
        extra_post_params: str | dict[str, dict[str, str]] | dict[str, str] = None,
        timeout=60.0,
    ) -> PlantIdentification | RawPlantIdentification | HealthAssessment | dict:
        identification = super().identify(
            image=image,
            details=self._build_details(details, disease_details),
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
            timeout=timeout,
        )
        if as_dict:
            return identification
        if classification_raw:
            return RawPlantIdentification.from_dict(identification)
        if health == 'only':
            return HealthAssessment.from_dict(identification)
        return PlantIdentification.from_dict(identification)

    def get_identification(
        self,
        token: str | int,
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        as_dict: bool = False,
        extra_get_params: str | dict[str, str] = None,
        timeout=60.0,
    ) -> PlantIdentification | dict:
        identification = super().get_identification(
            token=token,
            details=self._build_details(details, disease_details),
            language=language,
            as_dict=True,
            extra_get_params=extra_get_params,
            timeout=timeout,
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
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
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
        extra_get_params: str | dict[str, str] = None,
        extra_post_params: str = None,
        timeout=60.0,
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
        response = self._make_api_call(url, 'POST', payload, timeout=timeout)
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
        extra_get_params: str | dict[str, str] = None,
        timeout=60.0,
    ) -> HealthAssessment | dict:
        query = self._build_query(
            details=details, language=language, full_disease_list=full_disease_list, extra_get_params=extra_get_params
        )
        url = f'{self.identification_url}/{token}{query}'
        response = self._make_api_call(url, 'GET', timeout=timeout)
        if not response.ok:
            raise ValueError(f'Error while getting a health assessment: {response.status_code=} {response.text=}')
        health_assessment = response.json()
        return health_assessment if as_dict else HealthAssessment.from_dict(health_assessment)

    def delete_health_assessment(
        self,
        identification: HealthAssessment | str | int,
        timeout=60.0,
    ) -> bool:
        return self.delete_identification(identification, timeout=timeout)

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.plant.json'

    @classmethod
    def available_disease_details(cls) -> list[dict[str, any]]:
        with open(settings.APP_DIR / 'resources' / f'views.plant.disease.json') as f:
            return json.load(f)
