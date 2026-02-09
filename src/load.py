import pandas as pd

# ============== LOAD ==============
def load_players(df: pd.DataFrame, conn) -> int:
    """Charge les joueurs dans la base de données.

    Args:
        df: DataFrame des joueurs.
        conn: Connexion MySQL.

    Returns:
        Nombre de lignes insérées.
    """
    cursor = conn.cursor()

    query = """
    INSERT INTO players
    (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date),
        country = VALUES(country),
        level = VALUES(level)
    """

    count = 0

    for _, row in df.iterrows():
        values = (
            int(row["player_id"]),
            row["username"],
            row["email"] if pd.notna(row["email"]) else None,
            row["registration_date"].strftime("%Y-%m-%d")
                if pd.notna(row["registration_date"]) else None,
            row["country"],
            int(row["level"]) if pd.notna(row["level"]) else None
        )

        cursor.execute(query, values)
        count += 1

    print(f"Charge {count} joueurs")
    return count



def load_scores(df: pd.DataFrame, conn) -> int:
    """Charge les scores dans la base de données.

    Args:
        df: DataFrame des scores.
        conn: Connexion MySQL.

    Returns:
        Nombre de lignes insérées.
    """
    cursor = conn.cursor()

    query = """
    INSERT INTO scores
    (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        played_at = VALUES(played_at),
        platform = VALUES(platform)
    """

    count = 0

    for _, row in df.iterrows():
        values = (
            row["score_id"],
            int(row["player_id"]),
            row["game"],
            int(row["score"]) if pd.notna(row["score"]) else None,
            int(row["duration_minutes"]) if pd.notna(row["duration_minutes"]) else None,
            row["played_at"].strftime("%Y-%m-%d %H:%M:%S")
                if pd.notna(row["played_at"]) else None,
            row["platform"]
        )

        cursor.execute(query, values)
        count += 1

    print(f"Charge {count} scores")
    return count

