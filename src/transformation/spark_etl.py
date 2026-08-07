from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
from sqlalchemy import create_engine

def run_spark_etl():
    print("--- Initializing PySpark Session ---")
    spark = SparkSession.builder \
        .appName("CourtVision-SparkETL") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .getOrCreate()
    
    raw_file_path = "data/raw/clean_atp_matches_2023.csv"
    if not os.path.exists(raw_file_path):
        print(f"Raw data file not found at {raw_file_path}.")
        spark.stop()
        return

    print(f"Extracting data from {raw_file_path} using PySpark...")
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(raw_file_path)

    print("Transforming data with PySpark DataFrames...")
    transformed_df = df.dropna(subset=["winner_id", "loser_id", "tourney_date"]) \
                       .withColumn("match_duration_minutes", col("minutes").cast("int"))

    cleaned_spark_df = transformed_df.select(
        col("tourney_id"),
        col("tourney_name").alias("tournament_name"),
        col("surface"),
        col("tourney_date").alias("match_date"),
        col("winner_id").cast("int"),
        col("winner_name"),
        col("winner_rank").cast("int"),
        col("loser_id").cast("int"),
        col("loser_name"),
        col("loser_rank").cast("int"),
        col("match_duration_minutes")
    )

    print(f"Cleaned row count in Spark: {cleaned_spark_df.count()}")
    
    # Safe Bridge to Postgres via Pandas
    print("Loading transformed data into PostgreSQL Star Schema...")
    pandas_clean_df = cleaned_spark_df.toPandas()

    db_url = "postgresql://postgres:postgres@localhost:5432/courtvision_db"
    engine = create_engine(db_url)

    pandas_clean_df.to_sql("stg_matches", engine, if_exists="replace", index=False)
    print("Successfully loaded transformed data into PostgreSQL table 'stg_matches'!")

    spark.stop()
    print("--- PySpark End-to-End ETL Pipeline Completed Successfully ---")

if __name__ == "__main__":
    run_spark_etl()