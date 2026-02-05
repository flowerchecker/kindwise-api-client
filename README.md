# Kindwise sdk for python

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/flowerchecker/kindwise-api-client)

Python SDK toolkit for integrating Kindwise API into your application. This Python SDK provides a convenient way to
interact with the Kindwise API for plant, insect, and mushroom identification. The SDK is organized into different
modules, each corresponding to a specific domain ([plant](https://web.plant.id/plant-identification-api/),
[insect](https://www.kindwise.com/insect-id), [mushroom](https://www.kindwise.com/mushroom-id)). You can always use our
API without our SDK, the documentation can be found on the following links:

- [plant.id](https://plant.id/docs)
- [insect.id](https://insect.kindwise.com/docs)
- [mushroom.id](https://mushroom.kindwise.com/docs)
- [crop.health](https://crop.kindwise.com/docs)

## Setup

### Install

```bash
pip install kindwise-api-client
```

If you want to use the router offline classifier:

```
pip install kindwise-api-client[router]
```

If you want to use async interface:

```
pip install kindwise-api-client[async]
```

### API key

The API key serves to identify your account and is required to make requests to the API. Get API key at
[admin.kindwise.com](https://admin.kindwise.com).

## Quick Start

To use Kindwise API, an active API key is needed. See the section [above](#api-key) on how to get an API key.

```python
from kindwise import PlantApi, PlantIdentification, UsageInfo

# initialize plant.id api
# "PLANT_API_KEY" environment variable can be set instead of specifying api_key
api = PlantApi(api_key='your_api_key')

# get usage information
usage: UsageInfo = api.usage_info()

# identify plant by image
latitude_longitude = (49.20340, 16.57318)
# pass the image as a path
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
- [insect.id](https://insect.kindwise.com)
- [mushroom.id](https://mushroom.kindwise.com)
- [crop.health](https://crop.kindwise.com)

Each system has its class, which is used to make requests to the API. Each class has the following methods:

| method                                                    | description                                                                         | return type        | plant.id           | insect.id          | mushroom.id        | crop.health        |
|-----------------------------------------------------------|-------------------------------------------------------------------------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| [`identify`](#identify)                                   | create new identification                                                           | `Identification`   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`get_identification`](#get_identification)               | get identification by token                                                         | `Identification`   | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`delete_identification`](#delete_identification)         | delete identification by token                                                      | boolean            | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`usage_info`](#usage_info)                               | get api key usage information                                                       | `UsageInfo`        | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`feedback`](#feedback)                                   | send feedback for identification                                                    | boolean            | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`health_assessment`](#health_assessment)                 | create health assessment identification                                             | `HealthAssessment` | :white_check_mark: | :x:                | :x:                | :x:                |
| [`get_health_assessment`](#get_health_assessment)         | get health assessment identification                                                | `HealthAssessment` | :white_check_mark: | :x:                | :x:                | :x:                |
| [`delete_health_assessment`](#delete_health_assessment)   | delete health assessment                                                            | boolean            | :white_check_mark: | :x:                | :x:                | :x:                |
| [`available_details`](#available_details)                 | details which can be used to specify additional information for `identify`          | dict               | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| [`available_disease_details`](#available_disease_details) | details which can be used to specify additional information for `health_assessment` | dict               | :white_check_mark: | :x:                | :x:                | :x:                |
| [`search`](#search)                                       | search for entity by query param in our database                                    | `SearchRecord`     | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                |
| [`get_kb_detail`](#get_kb_detail)                         | returns information about entity                                                    | `dict`             | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x:                |
| [`ask_question`](#ask_question)                           | conversation about the identification                                               | `Conversation`     | :white_check_mark: | :x:                | :x:                | :x:                |
| [`get_conversation`](#get_conversation)                   | retrieve the identification's conversation                                          | `Conversation`     | :white_check_mark: | :x:                | :x:                | :x:                |
| [`conversation_feedback`](#conversation_feedback)         | set conversation's feedback                                                         | `Conversation`     | :white_check_mark: | :x:                | :x:                | :x:                |
| [`delete_conversation`](#delete_conversation)             | deletes the conversation                                                            | `Conversation`     | :white_check_mark: | :x:                | :x:                | :x:                |

Datetime objects are created by method `datetime.fromtimestamp(timestamp)`. This means that datetime objects are in
local timezone.

## Documentation

### Identification

#### available_details

Returns details which can be used to specify additional information for `identify` method. `

```python
from kindwise import PlantApi

api = PlantApi()

available_details = api.available_details()
```

#### identify

Creates a new identification. In one identification, you can include up to 5 images.

```python
import base64
from datetime import datetime

from kindwise import PlantApi, PlantIdentification, ClassificationLevel

api = PlantApi(api_key='your_api_key')
# this creates one identification composed of 5 images(not 5 different identifications)
#
# as input image is accepted path to an image(str / pathlib.Path), base64 encoded stream(bytes/string), stream(bytes/string),
# or file object(supports read,seek and mode methods)
# or PIL.Image.Image object
# or list of images
images = ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg', 'path/to/image4.jpg', 'path/to/image5.jpg']

# details included in identification
details = ['common_names', 'taxonomy', 'image']

# disease details included in health identification(only used if health=True)
# disease_details parameter is only available for plant.id
disease_details = ['local_name', 'description', 'treatment', 'cause']

# specify up to 3 languages
language = ['en', 'cs']

# default for similar_images is True
similar_images = True

# where was an image taken
latitude_longitude = (49.20340, 16.57318)

# include health assessment in your identification by specifying health='all',
# also use health='only' to get HealthAssessment(health assessment only)
# health assessment is only available for plant.id
health = 'all'

# custom id is used to identify identification in your system, but can be replaced with access_token
custom_id = 123

# when was an image taken, datetime can be specified as a datetime object, timestamp, or string in ISO format
date_time = datetime.now()

# default image size is 1500px, can be turned off by setting max_image_size to None
# be aware that our API has limit 25Mpx(e.g. 5000px x 5000px)
max_image_size = 1500

# specify into what depth should be the plant classified
# choose from ClassificationLevel.SPECIES, ClassificationLevel.GENUS, ClassificationLevel.ALL
# default is ClassificationLevel.SPECIES
classification_level = ClassificationLevel.SPECIES
# in case of need to merge results for different taxon levels yourself, set classification_raw=True
# be aware that the result will be in type kindwise.models.RawPlantIdentification
classification_raw = False
# if our api will be ahead of this sdk and you do not want to wait for update,
# specify extra_get_params or extra_post_params
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

# identification created from PIL.Image.Image object
from PIL import Image

image = Image.open('path/to/image.jpg')
identification_from_pil: PlantIdentification = api.identify(image)

# identification created from image url
image_url = 'https://api.gbif.org/v1/image/cache/fit-in/500x/occurrence/4596837568/media/33ff3ad210e56b73ade6f9fe622c650e'
identification_from_url: PlantIdentification = api.identify(image_url)
```

When you don't want to wait until the identification is finished, you can specify `asynchronous=True` and
get `access_token`  or `custom_id` if specified and retrieve the answer later.

```python
from kindwise import PlantApi, PlantIdentification

api = PlantApi(api_key='your_api_key')

image = 'path/to/image.jpg'
identification: PlantIdentification = api.identify(image, asynchronous=True)
# now do something else
# ...
# and later get identification by access_token or custom_id
identification: PlantIdentification = api.get_identification(identification.access_token, details=['common_names'])
```

#### get_identification

Get identification by token. You can specify which details you want to get. We store your identifications for 6 months.

```python
from kindwise import PlantApi, PlantIdentification

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
from kindwise import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or Identification object
api.delete_identification(custom_id)
```

#### usage_info

Gives you information about your api key usage.

```python
from kindwise import PlantApi, UsageInfo

api = PlantApi(api_key='your_api_key')

usage_info: UsageInfo = api.usage_info()
```

#### feedback

Send feedback for identification. You can specify a comment(string) or rating(int) in feedback. At least one of comment
and rating must be specified. You can specify identification by access_token or custom_id.

```python
from kindwise import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or Identification object
api.feedback(custom_id, comment='comment', rating=5)
```

### Health Assessment

#### available_disease_details

Returns details which can be used to specify additional information for `health_assessment` method. Only available for
plant.id.

```python
from kindwise import PlantApi

api = PlantApi()

available_disease_details = api.available_disease_details()
```

#### health_assessment

Returns only health assessment for identification. Health assessment is only available for plant.id. `health_assessment`
method is similar to `identify` method, but it returns only health assessment. Details differs for each system.

```python
from datetime import datetime

from kindwise import PlantApi, HealthAssessment

api = PlantApi(api_key="your_api_key")
# the same as in identify method
images = [
    "path/to/image1.jpg",
    "path/to/image2.jpg",
    "path/to/image3.jpg",
    "path/to/image4.jpg",
    "path/to/image5.jpg",
]

# details included in identification
details = ["local_name", "description", "treatment", "cause", "image"]

# specify up to 3 languages
language = ["en", "cs"]

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
# specify extra_get_params or extra_post_params
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
from kindwise import PlantApi, HealthAssessment

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
from kindwise import PlantApi

api = PlantApi(api_key='your_api_key')

custom_id = 123  # also works with access_token or HealthAssessment object
api.delete_health_assessment(custom_id)
```

### Knowledge Base

#### search

Search for entity(e.g. `Taraxacum`) by query param in our database. You can specify language, limit and database type.

```python
from kindwise import PlantApi, SearchResult, PlantKBType

api = PlantApi(api_key='your_api_key')
kb_type = PlantKBType.PLANTS
limit = 10
search_result: SearchResult = api.search('Taraxacum', language='en', kb_type=kb_type, limit=limit)
```

#### get_kb_detail

Returns information about entity(e.g. `Taraxacum`) in our database. You can specify in what language you want the
result.

```python
from kindwise import PlantApi, SearchResult

api = PlantApi(api_key='your_api_key')
search_result: SearchResult = api.search('Taraxacum', language='en', limit=1)

# details can also be specified as a list of strings
details = 'common_names,taxonomy'

entity_details = api.get_kb_detail(search_result.entities[0].access_token, details, language='de')
```

### Conversation

#### ask_question

Ask a question to our ChatBot. ChatBot supports multiple backends and its configuration can be modified.

```python
from kindwise import PlantApi, Conversation

api = PlantApi(api_key="your_api_key")

# Firstly you need to have an access_token of identification about which you want to ask the question
identification = "identification_access_token"

# question is a question that you want to ask the ChatBot
question = "Is this plant edible?"
# model is a parameter that controls the model used for generating the answer. List of models can be found in the documentation.
model = "gpt-3.5-turbo.demo"
# You can specify an app name that will be used for chat-bot to specify who is he
app_name = "my_app"
# You can specify a prompt that will be used together with our prompt to generate the answer.
prompt = "You are an assistant for a plant identification app. Please answer the user's question."
# Temperature is a parameter that controls the randomness of the model.
# The higher the temperature, the more random the output.
temperature = 0.0

# The configuration parameters: model, app_name, prompt, temperature are optional
# and can be specified only for the first question.
conversation: Conversation = api.ask_question(
    identification,
    question,
    model=model,
    app_name=app_name,
    prompt=prompt,
    temperature=temperature,
)

# You can set a conversation's feedback(JSON)
api.conversation_feedback(identification, {'rating': 5, 'comment': 'Great conversation!'})

# You can retrieve the conversation later


# You can also delete the conversation
api.delete_conversation(identification)
```

#### get_conversation

```python
from kindwise import PlantApi, Conversation

api = PlantApi(api_key='your_api_key')

# Firstly you need to have an access_token of identification about which you want to ask the question
identification = "identification_access_token"

conversation: Conversation = api.get_conversation(identification)
```

#### conversation_feedback

```python
from kindwise import PlantApi, Conversation

api = PlantApi(api_key='your_api_key')

# Firstly you need to have an access_token of identification about which you want to ask the question
identification = "identification_access_token"

# You can set a conversation's feedback(JSON)
api.conversation_feedback(identification, {'rating': 5, 'comment': 'Great conversation!'})
```

#### delete_conversation

```python
from kindwise import PlantApi, Conversation

api = PlantApi(api_key='your_api_key')

# Firstly you need to have an access_token of identification about which you want to ask the question
identification = "identification_access_token"

# You can also delete the conversation
api.delete_conversation(identification)
```

### Router
If you are not sure which API should be used to process your images, you can
use offline the **Router** model available in 3 sizes (`tiny`, `small`, and `base`).

```python
from kindwise import Router, RouterSize

image_path = 'path/to/your/image.jpg'
router = Router(RouterSize.BASE, device='cpu')
print(router.identify(image_path).simple)

# {
#   'plant': 0.4546036422252655,
#   'unhealthy_plant': 0.3136405646800995,
#   'mushroom': 0.29126274585723877,
#   'crop': 0.19530339539051056,
#   'insect': 0.0014414122560992837,
#   'human': 0.0003646785335149616
# }

```

### Async Interface

The same available methods are also available in async interface. Here is an example of how to use it.

```python
import asyncio
from kindwise import AsyncPlantApi, PlantIdentification, UsageInfo

async def main():
    # initialize plant.id api
    # "PLANT_API_KEY" environment variable can be set instead of specifying api_key
    api = AsyncPlantApi(api_key='your_api_key')
    # get usage information
    usage: UsageInfo = await api.usage_info()

    # identify plant by image
    latitude_longitude = (49.20340, 16.57318)
    # pass the image as a path
    image_path = 'path/to/plant_image.jpg'
    # make identification
    identification: PlantIdentification = await api.identify(image_path, latitude_longitude=latitude_longitude)

    # get identification by a token with changed views
    # this method can be used to modify additional information in identification or to get identification from database
    # also works with identification.custom_id
    identification_with_different_views: PlantIdentification = await api.get_identification(identification.access_token)

    # delete identification
    await api.delete_identification(identification)  # also works with identification.access_token or identification.custom_id

if __name__ == "__main__":
    asyncio.run(main())
```
