import os
import pandas as pd

PROCESSED_DIR = os.path.join("data", "processed")
CURATED_DIR = os.path.join("data", "curated")


def process_gold_layer():
    """
    Aggregates Silver layer data into Gold layer curated analytics 
    (player win rates, surface-specific performance, etc.).
    """
    os.makedirs(CURATED_DIR, exist_ok=True)
    print("--- Starting Gold Layer Aggregations ---")

    # 1. Load clean match files for 2023 and 2024
    match_files = ["clean_atp_matches_2023.csv", "clean_atp_matches_2024.csv"]
    df_list = []
    
    for file in match_files:
        path = os.path.join(PROCESSED_DIR, file)
        if os.path.exists(path):
            df = pd.read_csv(path, low_memory=False)
            df_list.append(df)
            
    if not df_list:
        print("No processed match files found in data/processed/!")
        return

    matches_df = pd.concat(df_list, ignore_index=True)
    print(f"Loaded {len(matches_df):,} total matches for Gold aggregation.")

    # 2. Calculate Player Wins and Losses by Surface
    # Extract winners
    winners = matches_df[["winner_name", "surface"]].copy()
    winners.rename(columns={"winner_name": "player_name"}, inplace=True)
    winners["wins"] = 1
    winners["losses"] = 0

    # Extract losers
    losers = matches_df[["loser_name", "surface"]].copy()
    losers.rename(columns={"loser_name": "player_name"}, inplace=True)
    losers["wins"] = 0
    losers["losses"] = 1

    # Combine into a unified match-outcome dataframe
    player_matches = pd.concat([winners, losers], ignore_index=True)

    # Group by player and surface to compute stats
    surface_stats = player_matches.groupby(["player_name", "surface"]).agg(
        wins=("wins", "sum"),
        losses=("losses", "sum")
    ).reset_index()

    surface_stats["total_matches"] = surface_stats["wins"] + surface_stats["losses"]
    surface_stats["win_rate"] = (surface_stats["wins"] / surface_stats["total_matches"]).round(4)

    # Save surface performance stats
    surface_output_path = os.path.join(CURATED_DIR, "player_surface_stats.csv")
    surface_stats.to_csv(surface_output_path, index=False)
    print(f"Saved Curated Surface Stats -> {surface_output_path}")

    # 3. Calculate Overall Player Career Summary (Across all surfaces)
    career_stats = player_matches.groupby("player_name").agg(
        total_wins=("wins", "sum"),
        total_losses=("losses", "sum")
    ).reset_index()

    career_stats["total_matches"] = career_stats["total_wins"] + career_stats["total_losses"]
    career_stats["career_win_rate"] = (career_stats["total_wins"] / career_stats["total_matches"]).round(4)
    career_stats = career_stats.sort_values(by="total_wins", ascending=False)

    # Save career summary stats
    career_output_path = os.path.join(CURATED_DIR, "player_career_stats.csv")
    career_stats.to_csv(career_output_path, index=False)
    print(f"Saved Curated Career Stats -> {career_output_path}")

    print("--- Gold Layer Aggregations Complete ---")


if __name__ == "__main__":
    process_gold_layer()