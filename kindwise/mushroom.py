import enum
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePath
from typing import BinaryIO

from PIL import Image

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import (
    Identification,
    Conversation,
    ResultEvaluation,
    Classification,
    Input,
    IdentificationStatus,
    Feedback,
)


class MushroomKBType(str, enum.Enum):
    MUSHROOM = 'mushroom'


@dataclass
class MushroomResult:
    is_mushroom: ResultEvaluation
    classification: Classification

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            is_mushroom=ResultEvaluation.from_dict(data['is_mushroom']),
            classification=Classification.from_dict(data['classification']),
        )


@dataclass
class MushroomIdentification(Identification):
    result: MushroomResult | None
    input: Input

    @classmethod
    def from_dict(cls, data: dict) -> 'MushroomIdentification':
        return cls(
            access_token=data['access_token'],
            model_version=data['model_version'],
            custom_id=data['custom_id'],
            input=Input.from_dict(data['input']),
            result=None if 'result' not in data else MushroomResult.from_dict(data['result']),
            status=IdentificationStatus(data['status']),
            sla_compliant_client=data['sla_compliant_client'],
            sla_compliant_system=data['sla_compliant_system'],
            created=datetime.fromtimestamp(data['created']),
            completed=None if data['completed'] is None else datetime.fromtimestamp(data['completed']),
            feedback=Feedback.from_dict(data['feedback']) if 'feedback' in data else None,
        )


class MushroomApi(KindwiseApi[Identification, MushroomKBType]):
    host = 'https://mushroom.kindwise.com'
    default_kb_type = MushroomKBType.MUSHROOM

    def __init__(self, api_key: str = None):
        api_key = settings.MUSHROOM_API_KEY if api_key is None else api_key
        if api_key is None:
            raise ValueError(
                'API key is required, set it in init method of class or in .env file under "MUSHROOM_API_KEY" key'
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
        return settings.APP_DIR / 'resources' / f'views.mushroom.json'

    @property
    def kb_api_url(self):
        return f'{self.host}/api/v1/kb'

    def identify(
        self,
        image: PurePath | str | bytes | BinaryIO | Image.Image | list[str | PurePath | bytes | BinaryIO | Image.Image],
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        asynchronous: bool = False,
        similar_images: bool = True,
        latitude_longitude: tuple[float, float] = None,
        custom_id: int | None = None,
        date_time: datetime | str | float | None = None,
        max_image_size: int | None = 1500,
        as_dict: bool = False,
        extra_get_params: str | dict[str, str] = None,
        extra_post_params: str | dict[str, dict[str, str]] | dict[str, str] = None,
    ) -> MushroomIdentification | dict:
        identification = super().identify(
            image=image,
            details=details,
            language=language,
            asynchronous=asynchronous,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            custom_id=custom_id,
            date_time=date_time,
            max_image_size=max_image_size,
            as_dict=True,
            extra_get_params=extra_get_params,
            extra_post_params=extra_post_params,
        )
        if as_dict:
            return identification
        return MushroomIdentification.from_dict(identification)

    def get_identification(
        self,
        token: str | int,
        details: str | list[str] = None,
        disease_details: str | list[str] = None,
        language: str | list[str] = None,
        as_dict: bool = False,
        extra_get_params: str | dict[str, str] = None,
    ) -> MushroomIdentification | dict:
        identification = super().get_identification(
            token=token,
            details=details,
            language=language,
            as_dict=True,
            extra_get_params=extra_get_params,
        )
        return identification if as_dict else MushroomIdentification.from_dict(identification)

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.mushroom.json'

    def ask_question(
        self,
        identification: Identification | str | int,
        question: str,
        model: str = None,
        app_name: str = None,
        prompt: str = None,
        temperature: float = None,
        as_dict: bool = False,
    ) -> Conversation:
        raise NotImplementedError('Asking questions is currently not supported by mushroom.id')
