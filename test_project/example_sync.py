from dotenv import load_dotenv
from kindwise import PlantApi, PlantIdentification

# Load environment variables from .env file
load_dotenv()


def main():
    # Initialize PlantApi
    # The library will automatically read PLANT_API_KEY from the environment variables
    # ensuring the api_key is not hardcoded.
    api = PlantApi()

    print("PlantApi initialized.")
    if api.api_key:
        print("API Key successfully loaded from environment.")
    else:
        print("Warning: API Key not found. Please check your .env file.")
        return

    # Example: Identify plant from file
    # Using a local image file provided in the directory
    image_path = 'image.jpg'

    print(f"Identifying plant from file: {image_path}")
    try:
        identification: PlantIdentification = api.identify(image_path, details=['common_names', 'url'])

        print("Identification successful!")
        print(f"Access Token: {identification.access_token}")

        if identification.result and identification.result.classification:
            best_match = identification.result.classification.suggestions[0]
            print(f"Best match: {best_match.name}")
            print(f"Probability: {best_match.probability}")

    except Exception as e:
        print(f"An error occurred during identification: {e}")


if __name__ == "__main__":
    main()
