from typing import List, Dict
from collections import defaultdict

class RepoRankingService:
    @staticmethod
    def rank_repositories(events: List[Dict]) -> List[Dict]:
        """Classe les dépôts par niveau d'activité."""
        repo_stats = defaultdict(lambda: {
            "commits": 0,
            "issues": 0,
            "prs": 0,
            "total_activity": 0,
            "last_activity": None
        })
        
        for event in events:
            repo = event["repo_name"]
            event_date = event["created_at"]
            
            # Mise à jour de la dernière activité
            if not repo_stats[repo]["last_activity"] or event_date > repo_stats[repo]["last_activity"]:
                repo_stats[repo]["last_activity"] = event_date
            
            # Calcul des statistiques par type d'événement
            if event["type"] == "PushEvent":
                repo_stats[repo]["commits"] += event["details"]["commits"]
            elif event["type"] == "IssuesEvent" and event["details"]["action"] == "opened":
                repo_stats[repo]["issues"] += 1
            elif event["type"] == "PullRequestEvent" and event["details"]["action"] == "opened":
                repo_stats[repo]["prs"] += 1
            
            # Calcul du score d'activité pondéré
            repo_stats[repo]["total_activity"] = (
                repo_stats[repo]["commits"] * 1 +  # Poids standard pour les commits
                repo_stats[repo]["issues"] * 2 +   # Poids plus élevé pour les issues
                repo_stats[repo]["prs"] * 3        # Poids le plus élevé pour les PRs
            )
        
        # Conversion et tri des résultats
        ranked_repos = [
            {"repo": repo, **stats}
            for repo, stats in repo_stats.items()
        ]
        
        return sorted(
            ranked_repos,
            key=lambda x: (x["total_activity"], x["last_activity"]),
            reverse=True
        ) 