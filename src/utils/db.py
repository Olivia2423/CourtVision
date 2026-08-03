import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "courtvision_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Build Database Connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_db_engine() -> Engine:
    """
    Creates and returns a SQLAlchemy database engine.
    """
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise e


def test_connection():
    """
    Tests the connection to PostgreSQL and prints the version.
    """
    engine = get_db_engine()
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            db_version = result.fetchone()
            print("Successfully connected to PostgreSQL!")
            print(f"PostgreSQL Version: {db_version[0]}")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")


if __name__ == "__main__":
    test_connection()