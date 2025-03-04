import os
from dotenv import load_dotenv
from api.github_client import GitHubClient
from models.event import EventProcessor
from services.event_service import EventFilterService
from services.stats_service import StatsService
from services.visualization_service import VisualizationService
from services.export_service import ExportService

def main():
    # Charger le token GitHub depuis les variables d'environnement (optionnel)
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')

    # Initialiser le client GitHub
    client = GitHubClient(token=github_token)

    while True:
        try:
            # Demander le nom d'utilisateur
            username = input("Entrez le nom d'utilisateur GitHub à analyser : ")
            
            # Demander la période
            print("\nPériodes disponibles : 24h, 48h, 1w, 2w, 30d")
            timeframe = input("Choisissez une période (30d par défaut) : ") or "30d"

            # Récupérer et traiter les événements
            print("\nRécupération des données...")
            raw_events = client.get_user_events(username)
            
            # Traiter chaque événement
            events = [EventProcessor.process_event(event) for event in raw_events]
            
            # Filtrer par période
            filtered_events = EventFilterService.filter_by_timeframe(events, timeframe)
            
            if not filtered_events:
                print(f"\nAucune activité trouvée pour {username} dans la période {timeframe}")
                continue

            # Calculer les statistiques
            print("\nCalcul des statistiques...")
            stats = StatsService.calculate_global_stats(filtered_events)
            
            # Afficher les statistiques de base
            print(f"\nStatistiques pour {username} (derniers {timeframe}):")
            print(f"Total des commits : {stats['total_commits']}")
            print(f"Issues créées : {stats['total_issues']}")
            print(f"Pull Requests : {stats['total_prs']}")
            print(f"Nombre de dépôts actifs : {stats['total_repos']}")

            # Générer les visualisations
            print("\nGénération des visualisations...")
            hist_path = VisualizationService.create_commit_histogram(filtered_events, timeframe)
            pie_path = VisualizationService.create_activity_pie_chart(stats)
            timeline_path = VisualizationService.create_activity_timeline(filtered_events)

            # Exporter les données
            print("\nExport des données...")
            csv_path = ExportService.to_csv(filtered_events)
            json_path = ExportService.to_json(filtered_events)
            pdf_path = ExportService.to_pdf(stats)

            print("\nFichiers générés :")
            print(f"Histogramme des commits : {hist_path}")
            print(f"Distribution des activités : {pie_path}")
            print(f"Timeline d'activité : {timeline_path}")
            print(f"Export CSV : {csv_path}")
            print(f"Export JSON : {json_path}")
            print(f"Export PDF : {pdf_path}")

            # Demander si l'utilisateur veut continuer
            if input("\nVoulez-vous analyser un autre utilisateur ? (o/N) : ").lower() != 'o':
                break

        except ValueError as e:
            print(f"\nErreur : {e}")
        except Exception as e:
            print(f"\nUne erreur est survenue : {e}")
            if input("\nVoulez-vous réessayer ? (o/N) : ").lower() != 'o':
                break

if __name__ == "__main__":
    main() 