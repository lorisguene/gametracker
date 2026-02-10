# 📘 GameTracker – Pipeline ETL Dockerisé (MySQL + Python)

GameTracker est une application qui nettoie et traite des données de joueurs et de sessions de jeux vidéo, les charge dans une base MySQL, puis génère automatiquement un rapport de synthèse.  
Le tout est entièrement **conteneurisé**, **automatisé** et **versionné**.

***

## 🚀 Objectifs du projet

Ce mini‑projet a pour but de mobiliser les compétences vues en séances :

*   **Docker** : conteneurisation d’une application Python
*   **Bash** : automatisation de tâches
*   **Docker Compose** : orchestration multi‑services
*   **Python + MySQL** : pipeline ETL complet
*   **Git/GitHub** : versionnement et livraison

***

## 📦 Prérequis techniques

*   Docker & Docker Compose installés
*   Git
*   Un compte GitHub pour héberger le dépôt
*   Aucun environnement Python local n’est nécessaire (tout tourne en containers)

***

## 🏗️ Structure du projet

    gametracker/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── .gitignore
    ├── data/
    │   └── raw/
    │       ├── Players.csv
    │       └── Scores.csv
    ├── scripts/
    │   ├── init-db.sql
    │   ├── wait-for-db.sh
    │   └── run_pipeline.sh
    ├── src/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── extract.py
    │   ├── transform.py
    │   ├── load.py
    │   ├── report.py
    │   └── main.py
    └── output/
        └── rapport.txt (généré automatiquement)

***

## 🗂️ Données fournies

### **Players.csv**

*   `player_id`
*   `username`
*   `email`
*   `registration_date`
*   `country`
*   `level`

### **Scores.csv**

*   `score_id`
*   `player_id` (référence)
*   `game`
*   `score`
*   `duration_minutes`
*   `played_at`
*   `platform`

***

## 🧹 Problèmes de qualité traités (7 exigences)

Le pipeline ETL corrige **tous les problèmes imposés** :

1.  Doublons dans Players et Scores
2.  Emails invalides (pas de `@`) → remplacés par `None`
3.  Dates incohérentes ou invalides → converties avec `errors='coerce'`
4.  Espaces parasites dans les usernames
5.  Scores négatifs ou nuls → supprimés
6.  Valeurs manquantes (email, score, dates…)
7.  Références orphelines → score avec player\_id inexistant supprimé avant insertion

***

## 🔁 Fonctionnement du pipeline ETL

Le pipeline complet est orchestré dans :

    src/main.py

Étapes :

### **1. EXTRACT**

Lecture des CSV via pandas, affichage du nombre de lignes.

### **2. TRANSFORM**

Nettoyage séparé :

*   `transform_players()`
*   `transform_scores()` (nécessite la liste des player_id valides)

### **3. LOAD**

Chargement MySQL avec :

*   `load_players()`
*   `load_scores()`

Insertion avec **ON DUPLICATE KEY UPDATE**.

***

## 📄 Rapport généré automatiquement

Le rapport est écrit dans :

    output/rapport.txt

Il contient :

*   Nombre de joueurs
*   Nombre de scores
*   Nombre de jeux
*   Top 5 des meilleurs scores
*   Score moyen par jeu
*   Répartition des joueurs par pays
*   Répartition des sessions par plateforme

***

## ⚙️ Scripts Bash

### **run_pipeline.sh**

Ce script exécute automatiquement :

1.  Attente de MySQL (`wait-for-db.sh`)
2.  Exécution du script SQL `init-db.sql`
3.  Lancement du pipeline ETL Python (`python3 -m src.main`)
4.  Génération du rapport (`generate_report()`)

***

## 🐳 Instruction de lancement du projet

```bash
docker compose up -d --build
docker compose exec app ./scripts/run_pipeline.sh
```

***

## 📤 GitHub

*   Le code complet
*   Les CSV dans `data/raw/`
*   Un README clair
*   Un historique Git propre (au moins un commit par étape du projet)

