# Development Book - GitHub Profile Analyzer

## Project Setup

### Initial Setup and Dependencies
```bash
pip install -r requirements.txt
```

```requirements.txt
requests==2.31.0
python-dotenv==1.0.0
pandas==2.1.4
matplotlib==3.8.2
plotly==5.18.0
flask==3.0.0
PyPDF2==3.0.1
python-dateutil==2.8.2
```

### Project Structure
```
github_analyzer/
├── .env                    # Environment variables (GitHub token)
├── requirements.txt        # Project dependencies
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── github_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── event.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── event_service.py
│   │   ├── stats_service.py
│   │   └── export_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── date_utils.py
│   │   └── formatters.py
│   └── web/
│       ├── __init__.py
│       ├── app.py
│       └── templates/
└── tests/
    └── __init__.py
```

## Phase 1: Core Functionality Implementation

### 1. GitHub API Client (Priority 1)
```python
# src/api/github_client.py
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
```

### 2. Event Processing (Priority 1)
```python
# src/models/event.py
from typing import TypedDict, List, Optional
from datetime import datetime

class GitHubEvent(TypedDict):
    id: str
    type: str
    created_at: str
    repo: dict
    payload: dict

class EventProcessor:
    @staticmethod
    def process_event(event: GitHubEvent) -> dict:
        """Process a GitHub event and extract relevant information."""
        created_at = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        
        return {
            "id": event["id"],
            "type": event["type"],
            "created_at": created_at,
            "repo_name": event["repo"]["name"],
            "details": EventProcessor._extract_event_details(event)
        }
    
    @staticmethod
    def _extract_event_details(event: GitHubEvent) -> dict:
        """Extract specific details based on event type."""
        event_type = event["type"]
        payload = event["payload"]
        
        if event_type == "PushEvent":
            return {
                "commits": len(payload.get("commits", [])),
                "ref": payload.get("ref", "")
            }
        elif event_type == "IssuesEvent":
            return {
                "action": payload.get("action", ""),
                "issue_number": payload.get("issue", {}).get("number")
            }
        # Add more event types as needed
        return {}
```

### 3. Date Filtering Service (Priority 1)
```python
# src/services/event_service.py
from datetime import datetime, timedelta
from typing import List, Dict

class EventFilterService:
    @staticmethod
    def filter_by_timeframe(events: List[Dict], timeframe: str) -> List[Dict]:
        """Filter events based on specified timeframe."""
        now = datetime.utcnow()
        timeframes = {
            "24h": timedelta(hours=24),
            "48h": timedelta(hours=48),
            "1w": timedelta(weeks=1),
            "2w": timedelta(weeks=2),
            "30d": timedelta(days=30)
        }
        
        if timeframe not in timeframes:
            raise ValueError(f"Invalid timeframe. Choose from: {', '.join(timeframes.keys())}")
        
        cutoff = now - timeframes[timeframe]
        return [event for event in events if event["created_at"] >= cutoff]
```

### 4. Statistics Service (Priority 1)
```python
# src/services/stats_service.py
from typing import List, Dict
from collections import defaultdict

class StatsService:
    @staticmethod
    def calculate_global_stats(events: List[Dict]) -> Dict:
        """Calculate global statistics from events."""
        stats = {
            "total_commits": 0,
            "total_issues": 0,
            "total_prs": 0,
            "total_repos": set(),
            "events_by_type": defaultdict(int)
        }
        
        for event in events:
            stats["events_by_type"][event["type"]] += 1
            stats["total_repos"].add(event["repo_name"])
            
            if event["type"] == "PushEvent":
                stats["total_commits"] += event["details"]["commits"]
            elif event["type"] == "IssuesEvent" and event["details"]["action"] == "opened":
                stats["total_issues"] += 1
            elif event["type"] == "PullRequestEvent" and event["details"]["action"] == "opened":
                stats["total_prs"] += 1
        
        stats["total_repos"] = len(stats["total_repos"])
        return dict(stats)
```

## Phase 2: Advanced Features

### 5. Repository Activity Ranking (Priority 2)
```python
# src/services/stats_service.py
class RepoActivityService:
    @staticmethod
    def rank_repositories(events: List[Dict]) -> List[Dict]:
        """Rank repositories by activity level."""
        repo_stats = defaultdict(lambda: {
            "commits": 0,
            "issues": 0,
            "prs": 0,
            "total_activity": 0
        })
        
        for event in events:
            repo = event["repo_name"]
            if event["type"] == "PushEvent":
                repo_stats[repo]["commits"] += event["details"]["commits"]
            elif event["type"] == "IssuesEvent":
                repo_stats[repo]["issues"] += 1
            elif event["type"] == "PullRequestEvent":
                repo_stats[repo]["prs"] += 1
                
            repo_stats[repo]["total_activity"] = (
                repo_stats[repo]["commits"] +
                repo_stats[repo]["issues"] * 2 +
                repo_stats[repo]["prs"] * 3
            )
        
        return sorted(
            [{"repo": k, **v} for k, v in repo_stats.items()],
            key=lambda x: x["total_activity"],
            reverse=True
        )
```

### 6. Data Export Service (Priority 2)
```python
# src/services/export_service.py
import json
import pandas as pd
from typing import List, Dict

class ExportService:
    @staticmethod
    def to_csv(data: List[Dict], filename: str) -> str:
        """Export data to CSV format."""
        df = pd.DataFrame(data)
        output_path = f"exports/{filename}.csv"
        df.to_csv(output_path, index=False)
        return output_path
    
    @staticmethod
    def to_json(data: List[Dict], filename: str) -> str:
        """Export data to JSON format."""
        output_path = f"exports/{filename}.json"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return output_path
```

### 7. Visualization Service (Priority 2)
```python
# src/services/visualization_service.py
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import List, Dict

class VisualizationService:
    @staticmethod
    def create_commit_histogram(events: List[Dict], timeframe: str) -> str:
        """Create histogram of commits over time."""
        commit_dates = [
            event["created_at"] for event in events
            if event["type"] == "PushEvent"
        ]
        
        plt.figure(figsize=(12, 6))
        plt.hist(commit_dates, bins=30)
        plt.title(f"Commit Activity ({timeframe})")
        plt.xlabel("Date")
        plt.ylabel("Number of Commits")
        
        output_path = "static/images/commit_histogram.png"
        plt.savefig(output_path)
        plt.close()
        return output_path
    
    @staticmethod
    def create_activity_pie_chart(stats: Dict) -> str:
        """Create pie chart of different activity types."""
        fig = go.Figure(data=[go.Pie(
            labels=list(stats["events_by_type"].keys()),
            values=list(stats["events_by_type"].values())
        )])
        
        output_path = "static/images/activity_distribution.html"
        fig.write_html(output_path)
        return output_path
```

## Phase 3: Web Interface

### 8. Flask Web Application (Priority 3)
```python
# src/web/app.py
from flask import Flask, render_template, request, jsonify
from src.api.github_client import GitHubClient
from src.services.stats_service import StatsService
from src.services.visualization_service import VisualizationService

app = Flask(__name__)
github_client = GitHubClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    username = request.form['username']
    timeframe = request.form.get('timeframe', '30d')
    
    try:
        events = github_client.get_user_events(username)
        filtered_events = EventFilterService.filter_by_timeframe(events, timeframe)
        stats = StatsService.calculate_global_stats(filtered_events)
        
        # Generate visualizations
        commit_hist = VisualizationService.create_commit_histogram(
            filtered_events, timeframe
        )
        activity_pie = VisualizationService.create_activity_pie_chart(stats)
        
        return render_template(
            'results.html',
            username=username,
            stats=stats,
            commit_hist=commit_hist,
            activity_pie=activity_pie
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

## Implementation Order and Dependencies

1. **Phase 1 (Core Functionality)**
   - GitHub API Client
   - Event Processing
   - Date Filtering
   - Basic Statistics

2. **Phase 2 (Advanced Features)**
   - Repository Activity Ranking
   - Data Export
   - Visualizations

3. **Phase 3 (Web Interface)**
   - Flask Setup
   - Templates
   - Interactive Dashboard

## Testing Strategy

Create unit tests for each component:

```python
# tests/test_github_client.py
import pytest
from src.api.github_client import GitHubClient

def test_github_client():
    client = GitHubClient()
    
    # Test successful API call
    events = client.get_user_events("testuser")
    assert isinstance(events, list)
    
    # Test error handling
    with pytest.raises(ValueError):
        client.get_user_events("nonexistentuser12345")
```

## Deployment Considerations

1. Environment Variables
```bash
# .env
GITHUB_TOKEN=your_token_here
FLASK_SECRET_KEY=your_secret_key
```

2. Production Setup
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    DEBUG = False
```

3. Error Handling
```python
# src/utils/error_handler.py
class GitHubAnalyzerError(Exception):
    """Base exception class for GitHub Analyzer."""
    pass

class RateLimitError(GitHubAnalyzerError):
    """Raised when GitHub API rate limit is exceeded."""
    pass

class UserNotFoundError(GitHubAnalyzerError):
    """Raised when GitHub user is not found."""
    pass
``` 