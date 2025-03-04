from datetime import datetime, timedelta
from typing import List, Dict

class EventFilterService:
    @staticmethod
    def filter_by_timeframe(events: List[Dict], timeframe: str) -> List[Dict]:
        """Filter events based on specified timeframe."""
        now = datetime.now()
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
    
    @staticmethod
    def filter_by_date_range(events: List[Dict], start_date: datetime, end_date: datetime) -> List[Dict]:
        """Filter events based on a specific date range."""
        return [
            event for event in events 
            if start_date <= event["created_at"] <= end_date
        ] 