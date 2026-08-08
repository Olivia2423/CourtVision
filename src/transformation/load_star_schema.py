from sqlalchemy import create_engine, text

def populate_star_schema():
    print("--- Starting Star Schema Population ---")
    
    db_url = "postgresql://postgres:Olivia@localhost:5432/courtvision_db"
    engine = create_engine(db_url)

    with engine.begin() as connection:
        print("Populating dim_tournament...")
        connection.execute(text("""
            INSERT INTO dim_tournament (tournament_id, tournament_name, surface_type)
            SELECT DISTINCT CAST(tourney_id AS INTEGER), tournament_name, surface
            FROM stg_matches
            WHERE tourney_id IS NOT NULL AND tourney_id ~ '^[0-9]+$'
            ON CONFLICT (tournament_id) DO NOTHING;
        """))

        print("Populating dim_surface...")
        connection.execute(text("""
            INSERT INTO dim_surface (surface_name)
            SELECT DISTINCT surface
            FROM stg_matches
            WHERE surface IS NOT NULL
            ON CONFLICT (surface_name) DO NOTHING;
        """))

        print("Populating dim_player (Winners & Losers)...")
        connection.execute(text("""
            INSERT INTO dim_player (player_id, player_name)
            SELECT DISTINCT winner_id AS player_id, winner_name AS player_name
            FROM stg_matches
            WHERE winner_id IS NOT NULL
            UNION
            SELECT DISTINCT loser_id AS player_id, loser_name AS player_name
            FROM stg_matches
            WHERE loser_id IS NOT NULL
            ON CONFLICT (player_id) DO NOTHING;
        """))

        print("Ensuring match_date column exists in fact_match...")
        connection.execute(text("""
            ALTER TABLE fact_match ADD COLUMN IF NOT EXISTS match_date DATE;
        """))

        print("Populating fact_match...")
        connection.execute(text("""
            INSERT INTO fact_match (
                tourney_id, match_date, winner_id, loser_id, 
                winner_rank, loser_rank, match_duration_minutes
            )
            SELECT 
                CAST(tourney_id AS INTEGER), 
                TO_DATE(match_date::text, 'YYYYMMDD') AS match_date,
                winner_id, 
                loser_id, 
                winner_rank, 
                loser_rank, 
                match_duration_minutes
            FROM stg_matches
            WHERE tourney_id IS NOT NULL 
              AND tourney_id ~ '^[0-9]+$'
              AND winner_id IS NOT NULL 
              AND loser_id IS NOT NULL;
        """))

    print("--- Star Schema Population Completed Successfully ---")

if __name__ == "__main__":
    populate_star_schema()