from pathlib import Path

from kindwise import settings
from kindwise.core import KindwiseApi


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

    @property
    def views_path(self) -> Path:
        return settings.APP_DIR / 'resources' / f'views.mushroom.json'
