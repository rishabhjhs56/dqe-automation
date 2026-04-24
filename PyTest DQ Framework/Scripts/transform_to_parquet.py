import pandas as pd
import psycopg2

db_params = {
    "host": "localhost",
    "port": 5432,
    "dbname": "mydatabase",
    "user": "postgres",
    "password": "postgres"
}

def fetch_data(query):
    conn = psycopg2.connect(**db_params)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def facility_type_avg_time_spent_per_visit_date():
    query = """
    SELECT f.facility_type, DATE(v.visit_timestamp) AS visit_date, AVG(v.duration_minutes) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    GROUP BY f.facility_type, DATE(v.visit_timestamp)
    """
    df = fetch_data(query)
    df.to_parquet("facility_type_avg_time_spent_per_visit_date.parquet")

if __name__ == "__main__":
    facility_type_avg_time_spent_per_visit_date()
    # Add other transformations as needed
