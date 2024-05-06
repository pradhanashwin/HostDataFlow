import requests
from typing import List

class QualysApiClient:
    def __init__(self, api_token: str, api_url: str):
        self.api_token = api_token
        self.api_url = api_url

    def fetch_hosts(self, skip: int = 1, limit: int = 1) -> List[dict]:
        headers = {"Token": f"{self.api_token}"}
        query_params = f"?skip={skip}&limit={limit}"
        
        # Create a session object
        session = requests.Session()

        # Set the headers for the session object
        session.headers.update(headers)
        # response = requests.get(self.api_url, headers=headers)
        response = session.post(self.api_url+query_params)
        response.raise_for_status()
        return response.json()

class CrowdstrikeApiClient:
    def __init__(self, api_token: str, api_url: str):
        self.api_token = api_token
        self.api_url = api_url

    def fetch_hosts(self, skip: int = 1, limit: int = 1) -> List[dict]:
        headers = {"Token": f"{self.api_token}"}
        query_params = f"?skip={skip}&limit={limit}"
        
        # Create a session object
        session = requests.Session()

        # Set the headers for the session object
        session.headers.update(headers)
        # response = requests.get(self.api_url, headers=headers)
        response = session.post(self.api_url+query_params)
        
        response.raise_for_status()
        return response.json()