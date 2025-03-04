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
        elif event_type == "PullRequestEvent":
            return {
                "action": payload.get("action", ""),
                "pr_number": payload.get("pull_request", {}).get("number")
            }
        return {} 