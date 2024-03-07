from dataclasses import dataclass
from pathlib import Path

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import Identification, ResultEvaluation, Classification


@dataclass
class CropResult:
    is_plant: ResultEvaluation
    is_healthy: ResultEvaluation | None
    crop: Classification
    disease: Classification | None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_plant=ResultEvaluation.from_dict(data['is_plant']),
            is_healthy=ResultEvaluation.from_dict(data['is_healthy']) if 'is_healthy' in data else None,
            crop=Classification.from_dict(data['crop']),
            disease=Classification.from_dict(data['disease']) if 'disease' in data else None,
        )


@dataclass
class CropIdentification(Identification):
    result: CropResult | None

    @classmethod
    def get_result_class(cls):
        return CropResult


class CropHealthApi(KindwiseApi):
    host = 'https://crop.kindwise.com'
    identification_class = CropIdentification

    def __init__(self, api_key: str = None):
        api_key = settings.CROP_HEALTH_API_KEY if api_key is None else api_key
        if api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "CROP_HEALTH_API_KEY" key'
            )
        super().__init__(api_key)

    def identify(self, *args, as_dict: bool = False, **kwargs) -> Identification | dict:
        identification = super().identify(*args, as_dict=True, **kwargs)
        if as_dict:
            return identification
        return CropIdentification.from_dict(identification)

    @property
    def identification_url(self):
        return f'{self.host}/api/v1/identification'

    @property
    def usage_info_url(self):
        return f'{self.host}/api/v1/usage_info'

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.crop_health.disease.json'
