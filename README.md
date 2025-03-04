# Analyseur de Profil GitHub

Un outil web pour analyser et visualiser l'activité d'un utilisateur GitHub. Cet outil permet d'obtenir des statistiques détaillées, des visualisations et des exports de données pour n'importe quel profil GitHub public.

![image](https://github.com/user-attachments/assets/a522ae63-cc7b-4986-bd05-c9a878b779b7)


## Fonctionnalités

- 📊 Statistiques globales (commits, PRs, issues, dépôts)
- 📈 Visualisations interactives
  - Histogramme des commits
  - Distribution des types d'activités
  - Timeline d'activité
- 💾 Export des données (CSV, JSON, PDF)
- 🎨 Interface moderne et responsive
- ⚡ Analyse rapide avec filtrage par période

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Un token GitHub (optionnel, mais recommandé)

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/github-profile-analyzer.git
cd github-profile-analyzer
```

2. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
# Créer un fichier .env à la racine du projet
touch .env

# Ajouter votre token GitHub (optionnel)
echo "GITHUB_TOKEN=votre_token_github" >> .env

# Ajouter une clé secrète pour Flask
echo "FLASK_SECRET_KEY=votre_cle_secrete" >> .env
```

## Utilisation

1. Lancer l'application :
```bash
cd src/web
python app.py
```

2. Ouvrir votre navigateur et accéder à :
```
http://localhost:5000
```

3. Entrer un nom d'utilisateur GitHub et choisir une période d'analyse

## Structure du projet

```
github_analyzer/
├── .env                    # Variables d'environnement
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
├── src/
│   ├── api/               # Client GitHub API
│   ├── models/            # Modèles de données
│   ├── services/          # Services métier
│   └── web/              # Interface web Flask
│       ├── static/        # Fichiers statiques
│       ├── templates/     # Templates HTML
│       └── app.py        # Application Flask
└── tests/                # Tests unitaires
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Si vous rencontrez des problèmes ou avez des questions :
1. Ouvrez une issue sur GitHub
2. Consultez la documentation
3. Contactez l'équipe de développement 
