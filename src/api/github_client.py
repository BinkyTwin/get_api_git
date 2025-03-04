from typing import Dict, List, Optional
import requests
from datetime import datetime

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}" if token else None
        }
    
    def get_user_events(self, username: str, page: int = 1) -> List[Dict]:
        """Fetch user events from GitHub API with pagination."""
        url = f"{self.base_url}/users/{username}/events"
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError("User not found")
        elif response.status_code == 403:
            raise Exception("Rate limit exceeded")
        else:
            raise Exception(f"API error: {response.status_code}") 