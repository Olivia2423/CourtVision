from sqlalchemy import text
from src.utils.db import get_db_engine

def create_advanced_views():
    """
    Creates Version 3 advanced analytical SQL views using CTEs and Window Functions.
    """
    print("--- Creating Version 3 Advanced Analytics Views ---")
    engine = get_db_engine()
    
    view_scripts = [
        """
        DROP VIEW IF EXISTS vw_player_surface_adaptability CASCADE;
        """,
        """
        CREATE VIEW vw_player_surface_adaptability AS
        WITH player_surface_breakdown AS (
            SELECT 
                p.player_id,
                p.player_name,
                s.surface_name,
                COUNT(*) as matches_played,
                SUM(CASE WHEN f.winner_id = p.player_id THEN 1 ELSE 0 END) as matches_won
            FROM fact_match f
            JOIN dim_player p ON f.winner_id = p.player_id OR f.loser_id = p.player_id
            JOIN dim_surface s ON f.surface_id = s.surface_id
            GROUP BY p.player_id, p.player_name, s.surface_name
        )
        SELECT 
            player_name,
            surface_name,
            matches_played,
            matches_won,
            ROUND((matches_won::NUMERIC / NULLIF(matches_played, 0)) * 100, 2) as win_percentage,
            RANK() OVER (PARTITION BY surface_name ORDER BY (matches_won::NUMERIC / NULLIF(matches_played, 0)) DESC) as rank_on_surface
        FROM player_surface_breakdown
        WHERE matches_played >= 5; -- Minimum threshold for meaningful ranking
        """,
        """
        DROP VIEW IF EXISTS vw_match_rankings_trend CASCADE;
        """,
        """
        CREATE VIEW vw_match_rankings_trend AS
        SELECT 
            f.match_id,
            d.full_date,
            t.tournament_name,
            w.player_name as winner_name,
            f.winner_rank,
            l.player_name as loser_name,
            f.loser_rank,
            -- Window function to calculate the running average match duration over time
            AVG(f.match_duration_minutes) OVER (ORDER BY d.full_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as rolling_avg_duration_10_matches
        FROM fact_match f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_tournament t ON f.tourney_id = t.tournament_name -- or match mapping
        JOIN dim_player w ON f.winner_id = w.player_id
        JOIN dim_player l ON f.loser_id = l.player_id
        WHERE f.match_duration_minutes IS NOT NULL;
        """
    ]

    try:
        with engine.begin() as conn:
            for sql in view_scripts:
                conn.execute(text(sql))
        print(" Successfully created advanced analytics views in PostgreSQL!")
    except Exception as e:
        print(f"Error creating analytical views: {e}")

if __name__ == "__main__":
    create_advanced_views()