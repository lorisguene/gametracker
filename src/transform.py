import pandas as pd


# ============== TRANSFORM : PLAYERS ==============
def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme et nettoie les données des joueurs.

    Args:
        df (pd.DataFrame): Données brutes issues de Players.csv

    Returns:
        pd.DataFrame: Données players nettoyées
    """
    df = df.copy()

    # 1. Supprimer doublons
    df = df.drop_duplicates(subset=["player_id"])
    

    # 2. Nettoyer les username
    df["username"] = df["username"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["username"])

    # 3. Convertir les dates
    df["registration_date"] = pd.to_datetime(
        df["registration_date"], errors="coerce"
    )

    # 4. Nettoyer les emails invalides
    df["email"] = df["email"].where(
        df["email"].str.contains("@", na=False), None
    )

    print(f"Transforme {len(df)} joueurs")
    return df


# ============== TRANSFORM : SCORES ==============
def transform_scores(df: pd.DataFrame, valid_player_ids: set) -> pd.DataFrame:
    """
    Transforme et nettoie les données des scores.


    Args:
        df (pd.DataFrame): Données brutes issues de Scores.csv
        valid_player_ids (set): Ensemble des player_id valides
                                issus du DataFrame players nettoyé.

    Returns:
        pd.DataFrame: Données scores nettoyées
    """
    df = df.copy()

    # 1. Supprimer doublons
    df = df.drop_duplicates(subset=["score_id"])
    


    # 2. Conversion des types
    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")

    # 3. Supprimer scores <= 0
    df = df[df["score"] > 0]

    # 4. Filtrer les player_id invalides
    df = df[df["player_id"].isin(valid_player_ids)]

    df = (
        df.sort_values(["score", "score_id"], ascending=[False, True])
        .drop_duplicates(subset=["player_id", "game", "played_at"], keep="first")
    )

    print(f"Transforme {len(df)} scores")
    return df