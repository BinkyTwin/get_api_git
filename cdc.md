# Cahier des Charges (CDC) – Outil d'Analyse de Profil GitHub

## 1. Contexte et Objectif

### 1.1 Contexte
De nombreux recruteurs et employeurs souhaitent évaluer les compétences techniques d’un candidat en analysant son activité sur GitHub. Cependant, il n’existe pas d’outil simple permettant de synthétiser et de visualiser rapidement les contributions d’un utilisateur GitHub.

### 1.2 Objectif du projet
Ce projet vise à fournir un outil permettant aux recruteurs et employeurs d’entrer le nom d’utilisateur GitHub d’un candidat et d’obtenir une analyse détaillée de son activité. L’outil devra afficher les statistiques clés, permettre un filtrage temporel et proposer une interface claire pour l’évaluation du profil technique.

---

## 2. Fonctionnalités

### Priorisation des fonctionnalités
Les fonctionnalités sont classées en trois niveaux de priorité :
- **Priorité 1 : Fonctionnalités de base**
- **Priorité 2 : Fonctionnalités avancées**
- **Priorité 3 : Fonctionnalités complexes nécessitant d'autres éléments**

### 2.1 Récupération et affichage des événements GitHub
- Connexion à l’API GitHub (`/users/{username}/events`)
- Récupération des types d'événements : **Push, Issues, Création de dépôts, Création de branches, Pull Requests**
- Stockage et affichage sous forme de texte

**Priorité : 1**  
**Dépendances : Aucune**  
**Difficulté : Facile**  

### 2.2 Ajout de la date de l’événement
- Ajout de la date (`created_at`) pour chaque événement
- Formatage en `JJ/MM/AAAA à HH:MM`
- Affichage dans les statistiques

**Priorité : 1**  
**Dépendances : Récupération des événements**  
**Difficulté : Facile**  

### 2.3 Filtrage des événements par période
- Filtrage des événements par :
  - 24 heures
  - 48 heures
  - 1 semaine
  - 2 semaines
  - 30 jours
- Comparaison entre `created_at` et la date actuelle

**Priorité : 1**  
**Dépendances : Ajout de la date**  
**Difficulté : Moyenne**  

### 2.4 Récupération des statistiques globales
- Nombre total de commits
- Nombre total d'issues ouvertes
- Nombre total de Pull Requests créées
- Nombre total de dépôts créés

**Priorité : 1**  
**Dépendances : Récupération des événements**  
**Difficulté : Moyenne**  

### 2.5 Classement des dépôts par activité
- Identifier les dépôts les plus actifs en fonction du nombre de commits, issues et Pull Requests
- Trier par ordre décroissant d'activité

**Priorité : 2**  
**Dépendances : Récupération des statistiques globales**  
**Difficulté : Intermédiaire**  

### 2.6 Export des données (CSV, JSON, PDF)
- Export des données sous différents formats :
  - CSV pour une analyse Excel
  - JSON pour une intégration API
  - PDF pour un rapport lisible

**Priorité : 2**  
**Dépendances : Récupération et traitement des données**  
**Difficulté : Intermédiaire**  

### 2.7 Affichage graphique des statistiques
- Génération de graphiques avec Matplotlib ou Plotly :
  - Histogramme des commits par jour
  - Diagramme circulaire des types d’activités
  - Courbe d’évolution des contributions

**Priorité : 2**  
**Dépendances : Statistiques globales**  
**Difficulté : Intermédiaire**  

### 2.8 Tableau de bord interactif
- Création d’une interface web dynamique avec Flask/Django
- Affichage sous forme de tableau de bord :
  - Graphiques
  - Filtres dynamiques
  - Classement des dépôts actifs
- Interaction en direct avec l’utilisateur

**Priorité : 3**  
**Dépendances : Export des données, affichage graphique**  
**Difficulté : Complexe**  

### 2.9 Ajout des Pull Requests (PR)
- Récupérer les Pull Requests créées, fusionnées et fermées
- Identifier les dépôts où l’utilisateur contribue le plus
- Afficher les PR associées aux commits

**Priorité : 3**  
**Dépendances : Récupération des événements, classement des dépôts**  
**Difficulté : Complexe**  

---

## 3. Contraintes techniques

### 3.1 API GitHub
- Utilisation de l’API REST GitHub (`/users/{username}/events`)
- Gestion de l'authentification via token GitHub pour éviter les limites de requêtes

### 3.2 Outils et bibliothèques
- **Python** : Langage principal
- **Requests** : Pour récupérer les données de l'API
- **Pandas** : Pour traiter les données et exporter en CSV
- **Matplotlib** : Pour les graphiques
- **Flask** : Pour le tableau de bord web

---

## 4. Conclusion
Ce projet a pour objectif de fournir un outil permettant aux recruteurs et employeurs d’analyser rapidement le profil GitHub d’un candidat. La première phase mettra en place les fonctionnalités de base, avant d’évoluer vers un tableau de bord interactif et une visualisation avancée des données.

---
