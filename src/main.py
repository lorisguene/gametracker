"""Pipeline principal GameTracker : Extract, Transform, Load."""

import os
from pathlib import Path

from .config import Config
from .extract import extract
from .transform import transform_players, transform_scores
from .load import load_players, load_scores
from .database import database_connection


def main():
    """Exécute le pipeline ETL complet."""

    print("=== Gametracker ETL : démarrage ===")

    # Création du dossier output/ si nécessaire
    Path("output").mkdir(exist_ok=True)

    # 1. Extract
    print("[1/3] Extraction des données...")
    players_raw = extract(os.path.join(Config.DATA_DIR, "Players.csv"))
    scores_raw = extract(os.path.join(Config.DATA_DIR, "Scores.csv"))

    # 2. Transform
    print("[2/3] Transformation des données...")
    players_clean = transform_players(players_raw)

    # Liste des IDs valides (entiers, uniques)
    valid_ids = (
        players_clean["player_id"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    scores_clean = transform_scores(scores_raw, valid_ids)

    # 3. Load
    print("[3/3] Chargement en base de données...")
    with database_connection() as conn:
        load_players(players_clean, conn)
        load_scores(scores_clean, conn)

    print("=== ETL terminé avec succès ===")


if __name__ == "__main__":
    main()