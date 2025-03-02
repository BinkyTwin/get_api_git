import requests

def afficher_data(username, dico, message):
    """
    Affiche les données stockées dans un dictionnaire.
    Si le dictionnaire est vide, un message spécifique est affiché.
    """
    if not dico:
        print(f"Aucune {message}.")
    else:
        for repo, count in dico.items():
            print(f"{username} {message} {count} fois dans {repo}.")


while True:
    username = input("Username recherché ? ")

    # URL de l'API GitHub pour récupérer les événements publics de l'utilisateur
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Convertir la réponse en format JSON
        
        # Dictionnaires pour stocker les données récupérées
        commit_repo = {}    # Stocke le nombre de commits par repo
        issues_repo = {}    # Stocke le nombre d'issues créées par repo
        creation_repo = {}  # Stocke le nombre de dépôts créés par repo
        branche_repo = {}   # Stocke le nombre de branches créées par repo

        # Parcours des événements retournés par l'API
        for event in data:
            repo_name = event["repo"]["name"]  # Récupération du nom du dépôt
            
            if event["type"] == "PushEvent":
                # Comptabilise le nombre de commits par dépôt
                commit_repo[repo_name] = commit_repo.get(repo_name, 0) + len(event["payload"].get("commits", []))

            elif event["type"] == "IssuesEvent" and event["payload"]["action"] == "opened":
                # Comptabilise le nombre d'issues créées par dépôt
                issues_repo[repo_name] = issues_repo.get(repo_name, 0) + 1

            elif event["type"] == "CreateEvent":
                # Vérifie si l'événement concerne un dépôt ou une branche
                ref_type = event["payload"]["ref_type"]
                if ref_type == "repository":
                    creation_repo[repo_name] = creation_repo.get(repo_name, 0) + 1
                elif ref_type == "branch":
                    branche_repo[repo_name] = branche_repo.get(repo_name, 0) + 1

        # Affichage des résultats
        afficher_data(username, commit_repo, "a poussé des commits")
        afficher_data(username, issues_repo, "a créé des issues")
        afficher_data(username, creation_repo, "a créé un dépôt")
        afficher_data(username, branche_repo, "a créé une branche")

        break  # Sortie de la boucle après une requête réussie

    elif response.status_code == 404:
        print("Utilisateur introuvable. Réessayez.")

    elif response.status_code == 403:
        print("Trop de requêtes ! Attendez ou utilisez un token GitHub.")
        break

    else:
        print(f"Erreur inattendue : {response.status_code}")
        break
