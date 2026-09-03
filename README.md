# CourtVision: End-to-End Tennis Data Engineering & Analytics Platform

CourtVision is an enterprise-grade data engineering and analytics platform designed to ingest, transform, model, and visualize extensive historical tennis match records. Built to handle over 547,000 matches, this project implements a complete modern data stack spanning distributed data pipelines, workflow orchestration, a relational star schema data warehouse, and dual-layer business intelligence reporting.

## Architecture & Data Flow

The platform follows a medallion-style data architecture, moving raw information through automated ingestion and transformation tiers before serving it to reporting layers:

Raw Data Sources -> PySpark (Bronze / Silver / Gold) -> Apache Airflow DAGs -> PostgreSQL Star Schema -> Power BI & Streamlit

1. **Ingestion & Processing (Bronze to Silver to Gold):** Scaled data cleaning, null handling, schema enforcement, and aggregations executed via **PySpark**.
2. **Orchestration:** Automated pipeline execution managed sequentially and dependently using **Apache Airflow**.
3. **Data Warehousing:** Curated models loaded into a normalized **PostgreSQL** star schema optimized for analytical queries.
4. **Presentation Layer:** Executive reporting delivered via an interactive **Power BI** dashboard and a custom programmatic **Streamlit** web application (`app.py`).

## Tech Stack

* **Big Data Processing:** Python, PySpark, Pandas, SQLAlchemy
* **Workflow Orchestration:** Apache Airflow
* **Data Warehousing:** PostgreSQL (Star Schema Architecture)
* **Business Intelligence & Visualization:** Power BI (Power Query, DAX, Custom Matrix & Slicers), Streamlit
* **Version Control & Tooling:** Git, GitHub, VS Code

## Repository Structure

```text
CourtVision/
│
├── dags/                    # Apache Airflow pipeline orchestration files
├── data/                    # Local staging and sample data assets
├── src/                     # PySpark ETL scripts and database connection modules
├── app.py                   # Interactive Streamlit analytics web application
├── requirements.txt         # Project Python dependencies
└── .gitignore               # Ignored system and configuration files
```

## Database Star Schema Design

The PostgreSQL data warehouse implements a star schema model to ensure high-performance analytical queries:

* **`fact_match`:** Core transaction table storing match results, durations, scores, and foreign keys pointing to dimension tables.
* **`dim_player`:** Normalized entity table storing player identifiers, names, and biographical attributes.
* **`dim_tournament`:** Dimension table mapping tournament names, tiers (Grand Slam, Masters, 250/500 levels), and metadata.
* **`dim_surface`:** Surface classification dimension tracking court conditions (Hard, Clay, Grass).

## Power BI Dashboard Highlights

![CourtVision Power BI Dashboard](https://github.com/user-attachments/assets/a6642173-59d2-402b-b40e-013890a702c7)

* **Executive KPI Header Cards:** Immediate visibility into **Total Matches**, overall **Win Rate**, **Total Wins**, and **Total Losses**.
* **Dynamic Slicing:** Left-aligned **Player Name** slicer that instantaneously filters the entire dashboard canvas.
* **Surface Breakdown Analysis:** Comparative bar charts evaluating player and tournament performance across Hard, Clay, and Grass courts.
* **Tournament Tier Segmentation:** Donut charts illustrating match distributions across tournament levels.
* **Expandable Date Matrix:** Hierarchical drill-down matrix displaying year, quarter, month, and day granularity mapped against specific tournament names.


## Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Olivia2423/CourtVision.git](https://github.com/Olivia2423/CourtVision.git)
   cd CourtVision
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit application locally:**
   ```bash
   streamlit run app.py
   ```

 **© 2026 Olivia Kewang. All rights reserved.*
   
