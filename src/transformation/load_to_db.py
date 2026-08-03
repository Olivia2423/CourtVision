import os
import pandas as pd
from src.utils.db import get_db_engine

PROCESSED_DIR = os.path.join("data", "processed")
CURATED_DIR = os.path.join("data", "curated")


def load_data_to_database():
    """
    Loads Silver and Gold datasets into the PostgreSQL database using the SQLAlchemy engine.
    """
    print("--- Starting Database Loading ---")
    
    try:
        engine = get_db_engine()
    except Exception as e:
        print(f"Failed to initialize database engine: {e}")
        return

    try:
        # 1. Load Gold Curated Career Stats
        career_path = os.path.join(CURATED_DIR, "player_career_stats.csv")
        if os.path.exists(career_path):
            print("Loading player_career_stats into PostgreSQL...")
            df_career = pd.read_csv(career_path)
            df_career.to_sql("player_career_stats", engine, if_exists="replace", index=False)
            print(" Successfully loaded player_career_stats.")

        # 2. Load Gold Curated Surface Stats
        surface_path = os.path.join(CURATED_DIR, "player_surface_stats.csv")
        if os.path.exists(surface_path):
            print("Loading player_surface_stats into PostgreSQL...")
            df_surface = pd.read_csv(surface_path)
            df_surface.to_sql("player_surface_stats", engine, if_exists="replace", index=False)
            print(" Successfully loaded player_surface_stats.")

        print("--- Database Loading Complete ---")

    except Exception as e:
        print(f"An error occurred while loading data to the database: {e}")


if __name__ == "__main__":
    load_data_to_database()