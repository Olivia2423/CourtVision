import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")


def process_silver_layer():
    """
    Cleans and standardizes raw Bronze layer datasets into the Silver processed layer.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("--- Starting Silver Layer Transformation ---")

    # 1. Process ATP Matches (2023 & 2024)
    match_files = ["atp_matches_2023.csv", "atp_matches_2024.csv"]
    for file in match_files:
        raw_path = os.path.join(RAW_DIR, file)
        if os.path.exists(raw_path):
            print(f"Processing match file: {file}...")
            df = pd.read_csv(raw_path, low_memory=False, encoding="latin-1")
            
            # Drop rows missing crucial match data
            if "winner_name" in df.columns and "loser_name" in df.columns:
                df = df.dropna(subset=["winner_name", "loser_name"])
            
            # Standardize tournament date format (YYYYMMDD to standard datetime)
            if "tourney_date" in df.columns:
                df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d", errors="coerce")
            
            # Save cleaned dataset to processed layer
            output_path = os.path.join(PROCESSED_DIR, f"clean_{file}")
            df.to_csv(output_path, index=False)
            print(f" Saved -> {output_path}")

    # 2. Process Player Database
    player_file = "atp_players_tml.csv"
    raw_player_path = os.path.join(RAW_DIR, player_file)
    if os.path.exists(raw_player_path):
        print(f"Processing player file: {player_file}...")
        df_players = pd.read_csv(raw_player_path, low_memory=False, encoding="latin-1")
        
        output_path = os.path.join(PROCESSED_DIR, "clean_atp_players.csv")
        df_players.to_csv(output_path, index=False)
        print(f" Saved -> {output_path}")

    # 3. Process Match Charting Project Data
    mcp_files = ["charting_m_matches.csv", "charting_m_points_2020s.csv"]
    for file in mcp_files:
        raw_path = os.path.join(RAW_DIR, file)
        if os.path.exists(raw_path):
            print(f"Processing charting file: {file}...")
            df_mcp = pd.read_csv(raw_path, low_memory=False, encoding="latin-1")
            
            output_path = os.path.join(PROCESSED_DIR, f"clean_{file}")
            df_mcp.to_csv(output_path, index=False)
            print(f" Saved -> {output_path}")

    print("--- Silver Layer Transformation Complete ---")


if __name__ == "__main__":
    process_silver_layer()