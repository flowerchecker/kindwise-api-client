import enum
from dataclasses import dataclass
from pathlib import Path

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import Identification, ResultEvaluation, ClassificationWithScientificName, Conversation


@dataclass
class CropResult:
    is_plant: ResultEvaluation
    crop: ClassificationWithScientificName
    disease: ClassificationWithScientificName | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_plant=ResultEvaluation.from_dict(data['is_plant']),
            crop=ClassificationWithScientificName.from_dict(data['crop']),
            disease=ClassificationWithScientificName.from_dict(data['disease']) if 'disease' in data else None,
        )


@dataclass
class CropIdentification(Identification):
    result: CropResult | None

    @classmethod
    def get_result_class(cls):
        return CropResult


class CropHealthKBType(str, enum.Enum):
    CROP = 'crop'


class CropHealthApi(KindwiseApi[CropIdentification, CropHealthKBType]):
    host = 'https://crop.kindwise.com'
    default_kb_type = CropHealthKBType.CROP
    identification_class = CropIdentification

    def __init__(self, api_key: str = None):
        api_key = settings.CROP_HEALTH_API_KEY if api_key is None else api_key
        if api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "CROP_HEALTH_API_KEY" key'
            )
        super().__init__(api_key)

    @property
    def identification_url(self):
        return f'{self.host}/api/v1/identification'

    @property
    def usage_info_url(self):
        return f'{self.host}/api/v1/usage_info'

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.crop_health.disease.json'

    @property
    def kb_api_url(self):
        raise NotImplementedError('Crop health API does not support knowledge base API')

    def ask_question(
        self,
        identification: CropIdentification | str | int,
        question: str,
        model: str = None,
        app_name: str = None,
        prompt: str = None,
        temperature: float = None,
        as_dict: bool = False,
        timeout=60.0,
    ) -> Conversation:
        raise NotImplementedError('Asking questions is currently not supported by crop.health.')
