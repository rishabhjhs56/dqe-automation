import shutil
from pathlib import Path

import pandas as pd

from src.connectors.postgres.postgres_connector import (
    PostgresConnectorContextManager
)

# ---------------------------------------------------
# Fixed Output Folder
# output/parquet/
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
PARQUET_BASE_DIR = OUTPUT_DIR / "parquet"


# ---------------------------------------------------
# Clean Old Output Every Run
# ---------------------------------------------------
def clean_old_output():
    if PARQUET_BASE_DIR.exists():
        shutil.rmtree(PARQUET_BASE_DIR)

    PARQUET_BASE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------
# Dataset 1
# ---------------------------------------------------
def facility_name_min_time_spent_per_visit_date(db_connection):
    query = """
    SELECT f.facility_name,
           DATE(v.visit_timestamp) AS visit_date,
           MIN(v.duration_minutes) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    WHERE v.visit_timestamp IS NOT NULL
      AND v.duration_minutes IS NOT NULL
    GROUP BY f.facility_name, DATE(v.visit_timestamp)
    """

    df = pd.read_sql(query, db_connection)

    df["visit_year_month"] = pd.to_datetime(
        df["visit_date"]
    ).dt.strftime("%Y-%m")

    out_dir = PARQUET_BASE_DIR / "facility_name_min_time_spent_per_visit_date"

    df.to_parquet(
        out_dir,
        partition_cols=["visit_year_month"],
        index=False,
        engine="pyarrow"
    )


# ---------------------------------------------------
# Dataset 2
# ---------------------------------------------------
def facility_type_avg_time_spent_per_visit_date(db_connection):
    query = """
    SELECT f.facility_type,
           DATE(v.visit_timestamp) AS visit_date,
           ROUND(AVG(v.duration_minutes), 2) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    WHERE v.visit_timestamp IS NOT NULL
      AND v.duration_minutes IS NOT NULL
    GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """

    df = pd.read_sql(query, db_connection)

    df["visit_year_month"] = pd.to_datetime(
        df["visit_date"]
    ).dt.strftime("%Y-%m")

    out_dir = PARQUET_BASE_DIR / "facility_type_avg_time_spent_per_visit_date"

    df.to_parquet(
        out_dir,
        partition_cols=["visit_year_month"],
        index=False,
        engine="pyarrow"
    )


# ---------------------------------------------------
# Dataset 3
# ---------------------------------------------------
def patient_sum_treatment_cost_per_facility_type(db_connection):
    query = """
    SELECT f.facility_type,
           CONCAT(p.first_name, ' ', p.last_name) AS full_name,
           SUM(v.treatment_cost) AS sum_treatment_cost
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    JOIN patients p ON v.patient_id = p.id
    WHERE v.treatment_cost IS NOT NULL
      AND v.treatment_cost >= 0
    GROUP BY f.facility_type, p.first_name, p.last_name
    """

    df = pd.read_sql(query, db_connection)

    out_dir = PARQUET_BASE_DIR / "patient_sum_treatment_cost_per_facility_type"

    df.to_parquet(
        out_dir,
        partition_cols=["facility_type"],
        index=False,
        engine="pyarrow"
    )


# ---------------------------------------------------
# Main
# ---------------------------------------------------
if __name__ == "__main__":
    print("Cleaning old parquet files...")
    clean_old_output()

    with PostgresConnectorContextManager() as conn:
        facility_name_min_time_spent_per_visit_date(conn)
        facility_type_avg_time_spent_per_visit_date(conn)
        patient_sum_treatment_cost_per_facility_type(conn)

    print(f"All partitioned Parquet files generated at: {PARQUET_BASE_DIR}")
