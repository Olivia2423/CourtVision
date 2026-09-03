# CourtVision: End-to-End Tennis Data Engineering & Analytics Platform

CourtVision is a data engineering and analytics platform designed to ingest, transform, model, and visualize historical tennis match data. The project demonstrates a modern data workflow spanning distributed data processing, pipeline orchestration, dimensional data warehousing, and interactive business intelligence reporting.

The complete pipeline processes more than 547,000 historical match records, while the current Power BI dashboard uses a curated reporting dataset for interactive analysis.

## Architecture and Data Flow

CourtVision follows a medallion-style data architecture that moves data through raw, cleaned, and analytics-ready layers:

Raw Data Sources → Apache Airflow-Orchestrated PySpark ETL → Bronze/Silver/Gold Data Layers → PostgreSQL Star Schema → Power BI and Streamlit

1. **Data Ingestion and Processing:** PySpark performs data ingestion, schema enforcement, null handling, cleaning, transformation, and aggregation across Bronze, Silver, and Gold data layers.

2. **Workflow Orchestration:** Apache Airflow manages task dependencies and coordinates the sequential execution of the data pipeline.

3. **Data Warehousing:** Curated analytical models are loaded into a dimensional PostgreSQL star schema optimized for reporting and analytical queries.

4. **Presentation Layer:** Insights are delivered through an interactive Power BI dashboard and a Streamlit web application defined in `app.py`.

## Tech Stack

* **Data Processing:** Python, PySpark, Pandas
* **Workflow Orchestration:** Apache Airflow
* **Database and Data Access:** PostgreSQL, SQL, SQLAlchemy
* **Business Intelligence:** Power BI, Power Query, DAX
* **Application Development:** Streamlit
* **Version Control and Tooling:** Git, GitHub, VS Code

## Repository Structure

~~~text
CourtVision/
│
├── dags/                    # Apache Airflow pipeline orchestration files
├── data/                    # Local staging and sample data assets
├── src/                     # PySpark ETL scripts and database modules
├── app.py                   # Interactive Streamlit analytics application
├── requirements.txt         # Python project dependencies
└── .gitignore               # Files excluded from version control
~~~

## Database Star Schema Design

The PostgreSQL data warehouse uses a dimensional star schema optimized for analytical queries:

* **`fact_match`:** Stores match results, dates, durations, scores, player references, surface references, and source tournament identifiers.
* **`dim_player`:** Stores player identifiers, names, handedness, and country information.
* **`dim_tournament`:** Stores tournament names, competition levels, surface classifications, and related metadata.
* **`dim_surface`:** Classifies court surfaces, including Hard, Clay, and Grass.

This structure separates measurable match activity from descriptive attributes, allowing Power BI to efficiently filter and aggregate results across players, tournaments, surfaces, and dates.

## Power BI Dashboard

![CourtVision Power BI Dashboard](https://github.com/user-attachments/assets/a6642173-59d2-402b-b40e-013890a702c7)

### Dashboard Highlights

* **Executive KPI Cards:** Display total matches, total wins, total losses, and overall win rate.
* **Dynamic Player Filtering:** A player-name slicer updates the dashboard to show an individual player’s matches, wins, losses, win rate, surface performance, and tournament results.
* **Surface Performance Analysis:** A bar chart compares wins across Hard, Clay, and Grass courts.
* **Tournament-Level Segmentation:** A donut chart displays the distribution of matches across tournament levels.
* **Tournament Performance Matrix:** A detailed matrix compares total wins and losses across tournaments.
* **Date Hierarchy Analysis:** Date fields support drill-down analysis by year, quarter, month, and day.

When no player is selected, the dashboard presents aggregate statistics for the complete reporting dataset. Because every completed match contains one winner and one loser, aggregate wins and losses are equal, producing an overall win rate of 50%.


## Project Purpose

CourtVision demonstrates the development of an end-to-end analytical solution, including:

* Processing large historical datasets with PySpark
* Orchestrating dependent data workflows with Apache Airflow
* Designing a dimensional PostgreSQL data warehouse
* Building relationships and analytical measures in Power BI
* Developing interactive reports with DAX, slicers, cards, charts, and matrices
* Delivering an additional analytics interface through Streamlit

## License

© 2026 Olivia Kewang. All rights reserved.
