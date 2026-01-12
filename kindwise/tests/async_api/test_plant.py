import random
from datetime import datetime

import pytest

from kindwise.async_api.plant import AsyncPlantApi, HealthAssessment, PlantIdentification
from kindwise.tests.conftest import IMAGE_DIR, environment_api, run_async_test_requests_to_server


@pytest.fixture
def image_path():
    return IMAGE_DIR / 'aloe-vera.jpg'


@pytest.fixture
def api(api_key):
    return AsyncPlantApi(api_key)


@pytest.mark.asyncio
async def test_requests_to_plant_server(api, image_path):
    await run_async_test_requests_to_server(api, 'plant', image_path, PlantIdentification)


@pytest.mark.asyncio
async def test_requests_to_plant_server__health_assessment(api, image_path):
    with environment_api(AsyncPlantApi(api), 'plant') as api:
        custom_id = random.randint(1000000, 2000000)
        date_time = datetime.now()
        print(f'Health assessment with {custom_id=} and {date_time=}:')
        health_assessment = await api.health_assessment(
            image_path,
            custom_id=custom_id,
            date_time=date_time,
            latitude_longitude=(49.20340, 16.57318),
            full_disease_list=True,
        )
        print(health_assessment)
        assert health_assessment.input.datetime == date_time
        assert health_assessment.input.similar_images
        assert health_assessment.input.latitude == 49.20340
        assert health_assessment.input.longitude == 16.57318
        assert health_assessment.custom_id == custom_id
        print()

        print('Feedback for health assessment:')
        assert await api.feedback(health_assessment.access_token, comment='correct', rating=5)

        health_assessment = await api.get_health_assessment(
            health_assessment.access_token, full_disease_list=True, language='cz', details=['treatment']
        )
        print('Health assessment with treatment details, cz language and full_disease_list:')
        print(health_assessment)
        print()
        assert isinstance(health_assessment, HealthAssessment)
        assert 'treatment' in health_assessment.result.disease.suggestions[0].details
        assert health_assessment.result.disease.suggestions[0].details['language'] == 'cz'
        assert health_assessment.feedback.comment == 'correct'
        assert health_assessment.feedback.rating == 5
        assert health_assessment.custom_id == custom_id
        assert health_assessment.input.datetime == date_time

        print('Deleting health assessment:')
        assert await api.delete_health_assessment(health_assessment.access_token)
        with pytest.raises(ValueError):
            await api.get_health_assessment(health_assessment.access_token)
