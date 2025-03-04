from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta

class StatsService:
    @staticmethod
    def calculate_global_stats(events: List[Dict]) -> Dict:
        """Calculate global statistics from events."""
        stats = {
            "total_commits": 0,
            "total_issues": 0,
            "total_prs": 0,
            "total_repos": set(),
            "events_by_type": defaultdict(int),
            "activity_by_day": defaultdict(int)
        }
        
        for event in events:
            event_date = event["created_at"].date()
            stats["events_by_type"][event["type"]] += 1
            stats["total_repos"].add(event["repo_name"])
            stats["activity_by_day"][event_date.isoformat()] += 1
            
            if event["type"] == "PushEvent":
                stats["total_commits"] += event["details"]["commits"]
            elif event["type"] == "IssuesEvent" and event["details"]["action"] == "opened":
                stats["total_issues"] += 1
            elif event["type"] == "PullRequestEvent" and event["details"]["action"] == "opened":
                stats["total_prs"] += 1
        
        stats["total_repos"] = len(stats["total_repos"])
        stats["activity_by_day"] = dict(stats["activity_by_day"])
        stats["events_by_type"] = dict(stats["events_by_type"])
        return stats
    
    @staticmethod
    def calculate_activity_trends(events: List[Dict], days: int = 30) -> Dict:
        """Calculate activity trends over time."""
        now = datetime.utcnow()
        start_date = now - timedelta(days=days)
        
        daily_activity = defaultdict(lambda: {
            "commits": 0,
            "issues": 0,
            "prs": 0,
            "total": 0
        })
        
        for event in events:
            if event["created_at"] < start_date:
                continue
                
            date = event["created_at"].date()
            date_str = date.isoformat()
            daily_activity[date_str]["total"] += 1
            
            if event["type"] == "PushEvent":
                daily_activity[date_str]["commits"] += event["details"]["commits"]
            elif event["type"] == "IssuesEvent" and event["details"]["action"] == "opened":
                daily_activity[date_str]["issues"] += 1
            elif event["type"] == "PullRequestEvent" and event["details"]["action"] == "opened":
                daily_activity[date_str]["prs"] += 1
        
        return dict(daily_activity) 