from sqlalchemy import text
from src.utils.db import get_db_engine

def create_star_schema():
    """
    Creates the Version 2 Star Schema (Fact and Dimension tables) in PostgreSQL.
    """
    print("--- Creating Data Warehouse Star Schema ---")
    
    engine = get_db_engine()
    
    ddl_statements = [
        """
        DROP TABLE IF EXISTS fact_match CASCADE;
        DROP TABLE IF EXISTS dim_player CASCADE;
        DROP TABLE IF EXISTS dim_tournament CASCADE;
        DROP TABLE IF EXISTS dim_surface CASCADE;
        DROP TABLE IF EXISTS dim_date CASCADE;
        """,
        """
        CREATE TABLE dim_player (
            player_id SERIAL PRIMARY KEY,
            player_name VARCHAR(255) UNIQUE NOT NULL,
            country_code VARCHAR(10),
            hand VARCHAR(10)
        );
        """,
        """
        CREATE TABLE dim_tournament (
            tournament_id SERIAL PRIMARY KEY,
            tournament_name VARCHAR(255) NOT NULL,
            surface_type VARCHAR(50),
            level VARCHAR(50)
        );
        """,
        """
        CREATE TABLE dim_surface (
            surface_id SERIAL PRIMARY KEY,
            surface_name VARCHAR(50) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE dim_date (
            date_id INT PRIMARY KEY,
            full_date DATE NOT NULL,
            year INT NOT NULL,
            month INT NOT NULL,
            day INT NOT NULL,
            quarter INT NOT NULL,
            day_of_week VARCHAR(20) NOT NULL
        );
        """,
        """
        CREATE TABLE fact_match (
            match_id SERIAL PRIMARY KEY,
            tourney_id VARCHAR(50),
            winner_id INT REFERENCES dim_player(player_id),
            loser_id INT REFERENCES dim_player(player_id),
            surface_id INT REFERENCES dim_surface(surface_id),
            date_id INT REFERENCES dim_date(date_id),
            match_duration_minutes INT,
            total_sets INT,
            winner_rank INT,
            loser_rank INT
        );
        """
    ]

    try:
        with engine.connect() as conn:
            for statement in ddl_statements:
                conn.execute(text(statement))
                conn.commit()
        print(" Successfully created all Fact and Dimension tables for Version 2!")
    except Exception as e:
        print(f"Error creating star schema: {e}")

if __name__ == "__main__":
    create_star_schema()