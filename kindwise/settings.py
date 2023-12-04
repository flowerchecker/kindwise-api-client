import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

PLANT_API_KEY = os.getenv('PLANT_API_KEY')
INSECT_API_KEY = os.getenv('INSECT_API_KEY')
MUSHROOM_API_KEY = os.getenv('MUSHROOM_API_KEY')

APP_DIR = Path(__file__).resolve().parent
