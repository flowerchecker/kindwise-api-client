from pathlib import Path
from datetime import datetime
from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import Identification


class MushroomApi(KindwiseApi):
    host = 'https://mushroom.kindwise.com'

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
    ) -> Identification:
        return super().identify(
            image=image,
            details=details,
            language=language,
            asynchronous=asynchronous,
            as_dict=as_dict,
            similar_images=similar_images,
            latitude_longitude=latitude_longitude,
            custom_id=custom_id,
            date_time=date_time,
        )
