import requests
import os

def fetch_images_by_breed(breed_id):
    """Fetch images for a specific breed from The Dog API."""
    api_key = os.getenv('DOG_API_KEY')
    headers = {'x-api-key': api_key}
    response = requests.get(
        f'https://api.thedogapi.com/v1/images/search?limit=5&breed_ids={breed_id}',
        headers=headers
    )
    if response.status_code == 200:
        images = response.json()
        print(f"API Response for breed_id={breed_id}: {images}")
        return images
    else:
        print(f"Error fetching images for breed_id={breed_id}: {response.status_code}")
        return []

def fetch_all_breeds():
    """Fetch all breeds from The Dog API."""
    api_key = os.getenv('DOG_API_KEY')
    headers = {'x-api-key': api_key}
    response = requests.get('https://api.thedogapi.com/v1/breeds', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching breeds: {response.status_code}")
        return []
