# Test Project for Kindwise SDK

This project demonstrates the basic usage of the Kindwise SDK (PlantApi and AsyncPlantApi) using a Python virtual environment.

## Setup

### 1. Create a Python Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# unix/macos
python3 -m venv venv
source venv/bin/activate
```

```bash
# windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

Install the required packages, including the Kindwise SDK and `python-dotenv`.

```bash
pip install -r requirements.txt
```


### 3. Configure API Key

Copy the example environment file and add your API Key.

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and replace `your_api_key_here` with your actual Kindwise Plant API Key.
   ```
   PLANT_API_KEY=your_actual_api_key_12345
   ```
   You can get an API key at [admin.kindwise.com](https://admin.kindwise.com).

## Running Examples

### Synchronous Client Example

The `example_sync.py` script demonstrates how to use `PlantApi` to identify a plant from an image URL.

```bash
python example_sync.py
```

### Asynchronous Client Example

The `example_async.py` script demonstrates how to use `AsyncPlantApi` with `asyncio`.

```bash
python example_async.py
```
