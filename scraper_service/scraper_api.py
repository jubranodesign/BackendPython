import requests

API_URL = "https://clinicaltrials.gov/api/v2/studies"


def fetch_studies(page_size: int = 5) -> list[dict]:
    params = {"pageSize": page_size, "format": "json"}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json().get("studies", [])

