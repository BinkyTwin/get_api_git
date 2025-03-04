from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys
from pathlib import Path
import json
from datetime import datetime, date

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.api.github_client import GitHubClient
from src.models.event import EventProcessor
from src.services.event_service import EventFilterService
from src.services.stats_service import StatsService
from src.services.visualization_service import VisualizationService
from src.services.export_service import ExportService
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_key')

# Personnaliser le JSONEncoder de Flask pour gérer les objets datetime
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# Initialiser le client GitHub
github_client = GitHubClient(token=os.getenv('GITHUB_TOKEN'))

@app.route('/')
def index():
    """Page d'accueil avec le formulaire d'analyse."""
    # Nettoyer la session à chaque visite de la page d'accueil
    session.clear()
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    """Analyser le profil GitHub et afficher les résultats."""
    username = request.form.get('username')
    timeframe = request.form.get('timeframe', '30d')
    
    if not username:
        return jsonify({"error": "Le nom d'utilisateur est requis"}), 400
    
    try:
        # Récupérer et traiter les événements
        raw_events = github_client.get_user_events(username)
        events = [EventProcessor.process_event(event) for event in raw_events]
        filtered_events = EventFilterService.filter_by_timeframe(events, timeframe)
        
        if not filtered_events:
            return jsonify({
                "error": f"Aucune activité trouvée pour {username} dans la période {timeframe}"
            }), 404
        
        # Calculer les statistiques
        stats = StatsService.calculate_global_stats(filtered_events)
        
        # Convertir les événements pour la session (rendre les objets datetime sérialisables)
        session_events = []
        for event in filtered_events:
            event_copy = event.copy()
            if isinstance(event_copy.get('created_at'), (datetime, date)):
                event_copy['created_at'] = event_copy['created_at'].isoformat()
            session_events.append(event_copy)
        
        # Stocker les données en session pour les exports
        session['filtered_events'] = session_events
        session['stats'] = stats
        
        # Générer les visualisations
        hist_path = VisualizationService.create_commit_histogram(filtered_events, timeframe)
        pie_path = VisualizationService.create_activity_pie_chart(stats)
        timeline_path = VisualizationService.create_activity_timeline(filtered_events)
        
        return render_template(
            'results.html',
            username=username,
            timeframe=timeframe,
            stats=stats,
            hist_path=hist_path,
            pie_path=pie_path,
            timeline_path=timeline_path
        )
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Une erreur est survenue : {str(e)}"}), 500

@app.route('/export/csv')
def export_csv():
    """Exporter les données au format CSV."""
    try:
        csv_path = ExportService.to_csv(session.get('filtered_events', []))
        return send_file(
            csv_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='github_activity.csv'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export/json')
def export_json():
    """Exporter les données au format JSON."""
    try:
        json_path = ExportService.to_json(session.get('filtered_events', []))
        return send_file(
            json_path,
            mimetype='application/json',
            as_attachment=True,
            download_name='github_activity.json'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export/pdf')
def export_pdf():
    """Exporter les données au format PDF."""
    try:
        pdf_path = ExportService.to_pdf(session.get('stats', {}))
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='github_activity.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 