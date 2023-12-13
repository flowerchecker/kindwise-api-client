# Kindwise sdk for python

Python SDK toolkit for integrating Kindwise API into your application. This Python SDK provides a convenient way to
interact with the Kindwise API for plant, insect, and mushroom identification. The SDK is organized into different
modules, each corresponding to a specific domain ([plant](https://web.plant.id/plant-identification-api/),
[insect](https://www.kindwise.com/insect-id), [mushroom](https://www.kindwise.com/mushroom-id)). You can always use our
API without our SDK, the documentation can be found on the following links:

- [plant](https://documenter.getpostman.com/view/24599534/2s93z5A4v2)
- [insect](https://documenter.getpostman.com/view/3802128/2s93sZ5YeU)
- [mushroom](https://documenter.getpostman.com/view/3802128/2s93kz55EY)

## Setup

### Install

```bash
pip install kindwise
```

### API key

The API key serves to identify your account and is required to make requests to the API. You can get your API key at
admin.kindwise.com. You need to register and create a new API key.

## Quick Start

To use Kindwise API, you need to have an active API key. If you already do not have any, see the API key section.

```python
from kindwise.plant import PlantApi
from kindwise.models import PlantIdentification, UsageInfo

# initialize plant.id api
# you do not have to specify api key here, if you have "PLANT_API_KEY" environment variable set.
api = PlantApi(api_key='your_api_key')

# get usage information
usage: UsageInfo = api.usage_info()

# identify plant by image
latitude_longitude = (49.20340, 16.57318)
# you must pass the image as a path
image_path = 'path/to/plant_image.jpg'
# make identification
identification: PlantIdentification = api.identify(image_path, latitude_longitude=latitude_longitude)

# get identification by a token with changed views
# this method can be used to modify additional information in identification or to get identification from database
# also works with identification.custom_id
identification_with_different_views: PlantIdentification = api.get_identification(identification.access_token)

# delete identification
api.delete_identification(identification)  # also works with identification.access_token or identification.custom_id
```

## Structure

SDK supports the following Kindwise systems:

- [plant.id](https://web.plant.id/plant-identification-api/)
- [insect.id](https://www.kindwise.com/insect-id)
- [mushroom.id](https://www.kindwise.com/mushroom-id)

Each system has its class, which is used to make requests to the API. Each class has the following methods:

| method                                                    | description                                                                         | return type        | plant              | insect             | mushroom           |
|-----------------------------------------------------------|-------------------------------------------------------------------------------------|--------------------|--------------------|--------------------|--------------------|
| [`identify`](#identify)                                   | create new identification                                                           | `Identification`   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`get_identification`](#get_identification)               | get identification by token                                                         | `Identification`   | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`delete_identification`](#delete_identification)         | delete identification by token                                                      | boolean            | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`usage_info`](#usage_info)                               | get api key usage information                                                       | `UsageInfo`        | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`feedback`](#feedback)                                   | send feedback for identification                                                    | boolean            | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`health_assessment`](#health_assessment)                 | create health assessment identification                                             | `HealthAssessment` | :white_check_mark: | :x:                | :x:                |
| [`get_health_assessment`](#get_health_assessment)         | get health assessment identification                                                | `HealthAssessment` | :white_check_mark: | :x:                | :x:                |
| [`delete_health_assessment`](#delete_health_assessment)   | delete health assessment                                                            | boolean            | :white_check_mark: | :x:                | :x:                |
| [`available_details`](#available_details)                 | details which can be used to specify additional information for `identify`          | dict               | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`available_disease_details`](#available_disease_details) | details which can be used to specify additional information for `health_assessment` | dict               | :white_check_mark: | :x:                | :x:                |

Datetime objects are created by method `datetime.fromtimestamp(timestamp)`. This means that datetime objects are in
local timezone.

### Documentation

#### available_details

Returns details which can be used to specify additional information for `identify` method. `

```python
from kindwise.plant import PlantApi

api = PlantApi()

available_details = api.available_details()
```

#### identify

Creates a new identification. In one identification, you can include up to 5 images.

```python
import base64
from datetime import datetime

from kindwise.models import PlantIdentification, ClassificationLevel
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')
# this creates one identification composed of 5 images(not 5 different identifications)
#
# as input image is accepted path to an image(str / pathlib.Path), base64 encoded stream(bytes/string), stream(bytes/string),
# or file object(supports read,seek and mode methods)
images = ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg', 'path/to/image4.jpg', 'path/to/image5.jpg']
# details included in identification
details = ['common_names', 'taxonomy', 'image']
# disease details included in health identification(only used if health=True)
# disease_details parameter is only available for plant.id
disease_details = ['local_name', 'description', 'treatment', 'cause']
# you can specify up to 3 languages
language = ['en', 'cs']
# default for similar_images is True
similar_images = True
# where was an image taken
latitude_longitude = (49.20340, 16.57318)
# you can include health assessment in your identification by specifying health=True,
# health assessment is only available for plant.id
health = True
# custom id is used to identify identification in your system, but can be replaced with access_token
custom_id = 123
# when was an image taken, datetime can be specified as a datetime object, timestamp, or string in ISO format
date_time = datetime.now()
# default image size is 1500px, can be turned off by setting max_image_size to None
# be aware that our API has limit 25Mpx(e.g. 5000px x 5000px)
max_image_size = 1500
# you can specify into what depth should be the plant classified
# you can choose from ClassificationLevel.SPECIES, ClassificationLevel.GENUS, ClassificationLevel.ALL
# default is ClassificationLevel.SPECIES
classification_level = ClassificationLevel.SPECIES
# in case you want to merge results for different taxon levels yourself, you can set classification_raw=True
# be aware that the result will be in type kindwise.models.RawPlantIdentification
classification_raw = False
# if our api will be ahead of this sdk and you do not want to wait for update,
# you can specify extra_get_params or extra_post_params
extra_get_params = None  # default
extra_post_params = None  # default
identification: PlantIdentification = api.identify(
    images,
    details=details,
    disease_details=disease_details,
    language=language,
    similar_images=similar_images,
    latitude_longitude=latitude_longitude,
    health=health,
    custom_id=custom_id,
    date_time=date_time,
    max_image_size=max_image_size,
    classification_level=classification_level,
    classification_raw=classification_raw,
    extra_get_params=extra_get_params,
    extra_post_params=extra_post_params,
)

# identification created from stream
with open('path/to/image.jpg', 'rb') as image:
    identification_from_stream: PlantIdentification = api.identify(image.read())

# identification created from file object
with open('path/to/image.jpg', 'rb') as image:
    identification_from_file: PlantIdentification = api.identify(image)

# identification created from base64 encoded image
with open('path/to/image.jpg', 'rb') as image:
    image_in_base64 = base64.b64encode(image.read())
    identification_from_base64: PlantIdentification = api.identify(image)
```

When you don't want to wait until the identification is finished, you can specify `asynchronous=True` and
get `access_token`  or `custom_id` if specified and retrieve the answer later.

```python
from kindwise.plant import PlantApi
from kindwise.models import PlantIdentification

api = PlantApi(api_key='your_api_key')

image = 'path/to/image.jpg'
identification: PlantIdentification = api.identify(image, asynchronous=True)
# now you can do something else
# ...
# and later get identification by access_token or custom_id
identification: PlantIdentification = api.get_identification(identification.access_token, details=['common_names'])
```

#### get_identification

Get identification by token. You can specify which details you want to get. We store your identifications for 6 months.

```python
from kindwise.models import PlantIdentification
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')

access_token = 'identification_access_token'
# details included in identification, can be different from used in identification create
details = ['common_names', 'taxonomy', 'image']
# language can also differ from used in identification create
language = 'de'
identification: PlantIdentification = api.get_identification(access_token, details=details, language=language)
```

#### delete_identification

Deletes identification from our database. You can specify identification by access_token or custom_id.

```python
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or Identification object
api.delete_identification(custom_id)
```

#### usage_info

Gives you information about your api key usage.

```python
from kindwise.plant import PlantApi
from kindwise.models import UsageInfo

api = PlantApi(api_key='your_api_key')

usage_info: UsageInfo = api.usage_info()
```

#### feedback

Send feedback for identification. You can specify a comment(string) or rating(int) in feedback. At least one of comment
and rating must be specified. You can specify identification by access_token or custom_id.

```python
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or Identification object
api.feedback(custom_id, comment='comment', rating=5)
```

#### available_disease_details

Returns details which can be used to specify additional information for `health_assessment` method. Only available for
plant.id.

```python
from kindwise.plant import PlantApi

api = PlantApi()

available_disease_details = api.available_disease_details()
```

#### health_assessment

Returns only health assessment for identification. Health assessment is only available for plant.id. `health_assessment`
method is similar to `identify` method, but it returns only health assessment. Details differs for each system.

```python
from datetime import datetime

from kindwise.models import HealthAssessment
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')
# the same as in identify method
images = ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg', 'path/to/image4.jpg', 'path/to/image5.jpg']
# details included in identification
details = ['local_name', 'description', 'treatment', 'cause', 'image']
# you can specify up to 3 languages
language = ['en', 'cs']
# default for similar_images is True
similar_images = True
# where was an image taken
latitude_longitude = (49.20340, 16.57318)
# custom id is used to identify identification in your system, but can be replaced with access_token
custom_id = 123
# list of suggested diseases also contains general diseases such as "Abiotic", default is False
full_disease_list = True
# when was an image taken, datetime can be specified as a datetime object, timestamp, or string in ISO format
date_time = datetime.now()
# default image size is 1500px, can be turned off by setting max_image_size to None
# be aware that our API has limit 25Mpx(e.g. 5000px x 5000px)
max_image_size = 1500
# if our api will be ahead of this sdk and you do not want to wait for update,
# you can specify extra_get_params or extra_post_params
extra_get_params = None  # default
extra_post_params = None  # default
identification: HealthAssessment = api.health_assessment(
    images,
    details=details,
    language=language,
    similar_images=similar_images,
    latitude_longitude=latitude_longitude,
    custom_id=custom_id,
    full_disease_list=full_disease_list,
    date_time=date_time,
    max_image_size=max_image_size,
)
```

When you don't want to wait until the identification is finished, you can specify `asynchronous=True` similar
to [`identify`](#identify) method.

#### get_health_assessment

Get a health assessment for identification. You can specify which details you want to get. We store your identifications
for 6 months.

```python
from kindwise.models import HealthAssessment
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')

access_token = 'identification_access_token'
# details included in identification can be different from those used in identification creation
details = ['classification', 'local_name']
# language can also differ from what is used in identification creation
language = 'de'
full_disease_list = False
identification: HealthAssessment = api.get_health_assessment(
    access_token,
    details=details,
    language=language,
    full_disease_list=full_disease_list
)
```

#### delete_health_assessment

Delete health assessment for identification.

```python
from kindwise.plant import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or HealthAssessment object
api.delete_health_assessment(custom_id)
```
