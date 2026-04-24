import pandas as pd
import os

def facility_name_min_time_spent_per_visit_date(db_connection):
    query = """
    SELECT f.facility_name,
           DATE(v.visit_timestamp) AS visit_date,
           MIN(v.duration_minutes) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    WHERE v.visit_timestamp IS NOT NULL AND v.duration_minutes IS NOT NULL
    GROUP BY f.facility_name, DATE(v.visit_timestamp)
    """
    df = pd.read_sql(query, db_connection)
    df['visit_year_month'] = pd.to_datetime(df['visit_date']).dt.strftime('%Y-%m')
    out_dir = "facility_name_min_time_spent_per_visit_date"
    os.makedirs(out_dir, exist_ok=True)
    df.to_parquet(
        out_dir,
        partition_cols=['visit_year_month'],
        index=False
    )

def facility_type_avg_time_spent_per_visit_date(db_connection):
    query = """
    SELECT f.facility_type,
           DATE(v.visit_timestamp) AS visit_date,
           ROUND(AVG(v.duration_minutes), 2) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    WHERE v.visit_timestamp IS NOT NULL AND v.duration_minutes IS NOT NULL
    GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """
    df = pd.read_sql(query, db_connection)
    df['visit_year_month'] = pd.to_datetime(df['visit_date']).dt.strftime('%Y-%m')
    out_dir = "facility_type_avg_time_spent_per_visit_date"
    os.makedirs(out_dir, exist_ok=True)
    df.to_parquet(
        out_dir,
        partition_cols=['visit_year_month'],
        index=False
    )

def patient_sum_treatment_cost_per_facility_type(db_connection):
    query = """
    SELECT f.facility_type,
           CONCAT(p.first_name, ' ', p.last_name) AS full_name,
           SUM(v.treatment_cost) AS sum_treatment_cost
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    JOIN patients p ON v.patient_id = p.id
    WHERE v.treatment_cost >= 0 AND v.treatment_cost IS NOT NULL
    GROUP BY f.facility_type, p.first_name, p.last_name
    """
    df = pd.read_sql(query, db_connection)
    out_dir = "patient_sum_treatment_cost_per_facility_type"
    os.makedirs(out_dir, exist_ok=True)
    df.to_parquet(
        out_dir,
        partition_cols=['facility_type'],
        index=False
    )

# --- Main entry point ---
if __name__ == "__main__":
    # If running as a script, connect directly (for pipeline, use fixture)
    import psycopg2
    db_params = {
        "host": "localhost",
        "port": 5432,
        "dbname": "mydatabase",
        "user": "postgres",
        "password": "postgres"
    }
    conn = psycopg2.connect(**db_params)
    facility_name_min_time_spent_per_visit_date(conn)
    facility_type_avg_time_spent_per_visit_date(conn)
    patient_sum_treatment_cost_per_facility_type(conn)
    conn.close()
    print("All partitioned Parquet files generated.")
