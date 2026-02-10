# src/report.py
from datetime import datetime
from .database import database_connection


def generate_report():
    output_path = "output/rapport.txt"

    with database_connection() as conn:
        cursor = conn.cursor()

        # --- Statistiques générales ---
        cursor.execute("SELECT COUNT(*) FROM players;")
        nb_players = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scores;")
        nb_scores = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT game) FROM scores;")
        nb_games = cursor.fetchone()[0]

        # --- Top 5 des meilleurs scores ---
        cursor.execute("""
            SELECT p.username, s.game, s.score
            FROM scores s
            JOIN players p ON s.player_id = p.player_id
            ORDER BY s.score DESC
            LIMIT 5;
        """)
        top_scores = cursor.fetchall()

        # --- Score moyen par jeu ---
        cursor.execute("""
            SELECT game, AVG(score)
            FROM scores
            GROUP BY game
            ORDER BY game;
        """)
        avg_per_game = cursor.fetchall()

        # --- Joueurs par pays ---
        cursor.execute("""
            SELECT country, COUNT(*)
            FROM players
            GROUP BY country
            ORDER BY COUNT(*) DESC;
        """)
        players_by_country = cursor.fetchall()

        # --- Sessions par plateforme ---
        cursor.execute("""
            SELECT platform, COUNT(*)
            FROM scores
            GROUP BY platform
            ORDER BY COUNT(*) DESC;
        """)
        sessions_by_platform = cursor.fetchall()

    # ====== Écriture du rapport ======
    with open(output_path, "w", encoding="utf-8") as f:

        f.write("=" * 60 + "\n")
        f.write("GAMETRACKER - Rapport de synthese\n")
        f.write(f"Genere le : {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")

        # --- Section Statistiques générales ---
        f.write("--- Statistiques generales ---\n")
        f.write(f"Nombre de joueurs : {nb_players}\n")
        f.write(f"Nombre de scores : {nb_scores}\n")
        f.write(f"Nombre de jeux : {nb_games}\n\n")

        # --- Section Top 5 ---
        f.write("--- Top 5 des meilleurs scores ---\n")
        for i, (username, game, score) in enumerate(top_scores, 1):
            f.write(f"{i}. {username} | {game} | {score}\n")
        f.write("\n")

        # --- Score moyen par jeu ---
        f.write("--- Score moyen par jeu ---\n")
        for game, avg_score in avg_per_game:
            f.write(f"{game} : {round(avg_score, 2)}\n")
        f.write("\n")

        # --- Joueurs par pays ---
        f.write("--- Joueurs par pays ---\n")
        for country, count in players_by_country:
            f.write(f"{country} : {count}\n")
        f.write("\n")

        # --- Sessions par plateforme ---
        f.write("--- Sessions par plateforme ---\n")
        for platform, count in sessions_by_platform:
            f.write(f"{platform} : {count}\n")
        f.write("\n")

    print(f"[OK] Rapport généré : {output_path}")