import pytest

from kindwise.router import Router

from .conftest import IMAGE_DIR

test_images = [
    ('crop', IMAGE_DIR / 'wheat.jpg'),
    ('insect', IMAGE_DIR / 'bee.jpeg'),
    ('mushroom', IMAGE_DIR / 'amanita_muscaria.jpg'),
    ('plant', IMAGE_DIR / 'aloe-vera.jpg'),
    ('unhealthy_plant', IMAGE_DIR / 'potato.late_blight.jpg'),
    ('unhealthy_plant', IMAGE_DIR / 'padli.png'),
]


@pytest.mark.parametrize('classifier_name,image_path', test_images)
def test_identify(classifier_name, image_path):
    router = Router(device='cpu')
    result = router.identify(image_path)
    assert (
        result.simple[classifier_name] > 0.5
    ), f"Expected high confidence for {classifier_name} on image {image_path}, got {result.simple[classifier_name]}"
