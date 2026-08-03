import os
import pandas as pd
from sqlalchemy import text
from src.utils.db import get_db_engine

PROCESSED_DIR = os.path.join("data", "processed")

def parse_date_to_id(val):
    """Helper to safely parse any date format into an YYYYMMDD integer (date_id)."""
    if pd.isna(val):
        return None, None
    try:
        # First, try standard pandas datetime inference
        dt = pd.to_datetime(val, errors='coerce')
        if pd.isna(dt):
            # Fallback: try stripping decimals if it's read as a float string like '20230102.0'
            val_str = str(val).split('.')[0]
            dt = pd.to_datetime(val_str, format='%Y%m%d', errors='coerce')
        
        if pd.isna(dt):
            return None, None
            
        date_id = int(dt.strftime('%Y%m%d'))
        return date_id, dt
    except Exception:
        return None, None

def populate_warehouse():
    """
    ETL script to populate the Star Schema warehouse tables from Silver layer data with robust date handling.
    """
    print("--- Starting Warehouse Population (ETL) ---")
    engine = get_db_engine()
    
    # 1. Load cleaned match data from Silver layer
    match_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.csv')]
    if not match_files:
        print("No processed files found in data/processed/")
        return
    
    target_file = match_files[0]
    print(f"Reading data from {target_file}...")
    df = pd.read_csv(os.path.join(PROCESSED_DIR, target_file))
    
    with engine.begin() as conn:
        # 2. Populate dim_surface
        print("Populating dim_surface...")
        surfaces = df['surface'].dropna().unique()
        for surface in surfaces:
            conn.execute(
                text("INSERT INTO dim_surface (surface_name) VALUES (:surface) ON CONFLICT (surface_name) DO NOTHING;"),
                {"surface": surface}
            )
        
        # 3. Populate dim_player (combining winners and losers)
        print("Populating dim_player...")
        winners = df[['winner_name']].rename(columns={'winner_name': 'player_name'})
        losers = df[['loser_name']].rename(columns={'loser_name': 'player_name'})
        players = pd.concat([winners, losers]).dropna().drop_duplicates()
        
        for _, row in players.iterrows():
            conn.execute(
                text("INSERT INTO dim_player (player_name) VALUES (:name) ON CONFLICT (player_name) DO NOTHING;"),
                {"name": row['player_name']}
            )
            
        # 4. Populate dim_tournament
        print("Populating dim_tournament...")
        tournaments = df[['tourney_name', 'surface', 'tourney_level']].drop_duplicates() if 'tourney_level' in df.columns else df[['tourney_name', 'surface']].drop_duplicates()
        for _, row in tournaments.iterrows():
            level = row.get('tourney_level', 'Unknown')
            conn.execute(
                text("""
                INSERT INTO dim_tournament (tournament_name, surface_type, level) 
                VALUES (:t_name, :surface, :level)
                ON CONFLICT DO NOTHING;
                """),
                {"t_name": row['tourney_name'], "surface": row['surface'], "level": level}
            )

        # 5. Populate dim_date flexibly
        print("Populating dim_date...")
        if 'tourney_date' in df.columns:
            unique_dates = df['tourney_date'].dropna().unique()
            for raw_date in unique_dates:
                date_id, dt = parse_date_to_id(raw_date)
                if date_id and dt:
                    conn.execute(
                        text("""
                        INSERT INTO dim_date (date_id, full_date, year, month, day, quarter, day_of_week)
                        VALUES (:d_id, :f_date, :year, :month, :day, :quarter, :dow)
                        ON CONFLICT (date_id) DO NOTHING;
                        """),
                        {
                            "d_id": date_id,
                            "f_date": dt.date(),
                            "year": dt.year,
                            "month": dt.month,
                            "day": dt.day,
                            "quarter": dt.quarter,
                            "dow": dt.day_name()
                        }
                    )

        print("Dimension tables populated successfully!")
        
        # 6. Populate fact_match using the robust parser
        print("Populating fact_match...")
        player_map = dict(conn.execute(text("SELECT player_name, player_id FROM dim_player;")).fetchall())
        surface_map = dict(conn.execute(text("SELECT surface_name, surface_id FROM dim_surface;")).fetchall())
        
        inserted_count = 0
        skipped_count = 0

        for _, row in df.iterrows():
            winner_id = player_map.get(row.get('winner_name'))
            loser_id = player_map.get(row.get('loser_name'))
            surface_id = surface_map.get(row.get('surface'))
            
            date_id, _ = parse_date_to_id(row.get('tourney_date'))
                
            if winner_id and loser_id and date_id:
                conn.execute(
                    text("""
                    INSERT INTO fact_match 
                    (tourney_id, winner_id, loser_id, surface_id, date_id, match_duration_minutes, total_sets, winner_rank, loser_rank)
                    VALUES (:t_id, :w_id, :l_id, :s_id, :d_id, :duration, :sets, :w_rank, :l_rank);
                    """),
                    {
                        "t_id": str(row.get('tourney_id', '')),
                        "w_id": winner_id,
                        "l_id": loser_id,
                        "s_id": surface_id,
                        "d_id": date_id,
                        "duration": int(row['minutes']) if pd.notna(row.get('minutes')) else None,
                        "sets": int(row['best_of']) if pd.notna(row.get('best_of')) else None,
                        "w_rank": int(row['winner_rank']) if pd.notna(row.get('winner_rank')) else None,
                        "l_rank": int(row['loser_rank']) if pd.notna(row.get('loser_rank')) else None
                    }
                )
                inserted_count += 1
            else:
                skipped_count += 1
                
        print(f" Successfully loaded {inserted_count:,} match rows into fact_match! (Skipped: {skipped_count})")

    print("--- Warehouse Population Complete ---")

if __name__ == "__main__":
    populate_warehouse()