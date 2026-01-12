import asyncio
from dotenv import load_dotenv
from kindwise import AsyncPlantApi, PlantIdentification

# Load environment variables from .env file
load_dotenv()


async def main():
    # Initialize AsyncPlantApi
    # The library will automatically read PLANT_API_KEY from the environment variables
    api = AsyncPlantApi()

    print("AsyncPlantApi initialized.")
    if api.api_key:
        print("API Key successfully loaded from environment.")
    else:
        print("Warning: API Key not found. Please check your .env file.")
        return

    # Example: Identify plant from file
    image_path = 'image.jpg'

    print(f"Identifying plant from file: {image_path}")
    try:
        identification: PlantIdentification = await api.identify(image_path, details=['common_names', 'url'])

        print("Identification successful!")
        print(f"Access Token: {identification.access_token}")

        if identification.result and identification.result.classification:
            best_match = identification.result.classification.suggestions[0]
            print(f"Best match: {best_match.name}")
            print(f"Probability: {best_match.probability}")

    except Exception as e:
        print(f"An error occurred during identification: {e}")

    # It's good practice to close the session if the API exposes such method,
    # but based on the README, there isn't an explicit close shown.
    # If the underlying implementation uses a session context manager, it should be fine.


if __name__ == "__main__":
    asyncio.run(main())
