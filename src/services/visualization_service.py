import matplotlib.pyplot as plt
import plotly.graph_objects as go
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

class VisualizationService:
    @staticmethod
    def ensure_output_dir(output_type: str) -> str:
        """Crée et retourne le chemin du répertoire de sortie."""
        base_dir = Path("static/images")
        output_dir = base_dir / output_type
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir)

    @staticmethod
    def create_commit_histogram(events: List[Dict], timeframe: str) -> str:
        """Crée un histogramme des commits dans le temps."""
        # Filtrer les événements de type Push
        commit_events = [
            event for event in events
            if event["type"] == "PushEvent"
        ]
        
        if not commit_events:
            return ""
        
        # Extraire les dates et le nombre de commits
        dates = [event["created_at"] for event in commit_events]
        commit_counts = [event["details"]["commits"] for event in commit_events]
        
        # Créer le graphique
        plt.figure(figsize=(12, 6))
        plt.hist(dates, bins=30, weights=commit_counts)
        plt.title(f"Activité des commits ({timeframe})")
        plt.xlabel("Date")
        plt.ylabel("Nombre de commits")
        plt.xticks(rotation=45)
        
        # Sauvegarder le graphique
        output_dir = VisualizationService.ensure_output_dir("matplotlib")
        output_path = f"{output_dir}/commit_histogram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
        return output_path

    @staticmethod
    def create_activity_pie_chart(stats: Dict) -> str:
        """Crée un diagramme circulaire des types d'activités."""
        if not stats.get("events_by_type"):
            return ""
        
        # Créer le graphique Plotly
        fig = go.Figure(data=[go.Pie(
            labels=list(stats["events_by_type"].keys()),
            values=list(stats["events_by_type"].values()),
            hole=0.3
        )])
        
        fig.update_layout(
            title="Distribution des types d'activités",
            showlegend=True,
            width=800,
            height=600
        )
        
        # Sauvegarder le graphique
        output_dir = VisualizationService.ensure_output_dir("plotly")
        output_path = f"{output_dir}/activity_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(output_path)
        
        return output_path

    @staticmethod
    def create_activity_timeline(events: List[Dict], days: int = 30) -> str:
        """Crée une timeline d'activité interactive."""
        # Préparer les données
        df = pd.DataFrame([{
            'date': event['created_at'].date(),
            'type': event['type'],
            'repo': event['repo_name']
        } for event in events])
        
        # Grouper par date et type
        daily_activity = df.groupby(['date', 'type']).size().unstack(fill_value=0)
        
        # Créer le graphique
        fig = go.Figure()
        
        for event_type in daily_activity.columns:
            fig.add_trace(go.Scatter(
                x=daily_activity.index,
                y=daily_activity[event_type],
                name=event_type,
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title="Timeline d'activité",
            xaxis_title="Date",
            yaxis_title="Nombre d'événements",
            hovermode='x unified',
            showlegend=True,
            width=1000,
            height=600
        )
        
        # Sauvegarder le graphique
        output_dir = VisualizationService.ensure_output_dir("plotly")
        output_path = f"{output_dir}/activity_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        fig.write_html(output_path)
        
        return output_path 