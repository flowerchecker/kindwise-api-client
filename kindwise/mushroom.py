import enum
from pathlib import Path

from kindwise import settings
from kindwise.core import KindwiseApi
from kindwise.models import Identification


class MushroomKBType(str, enum.Enum):
    MUSHROOM = 'mushroom'


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
