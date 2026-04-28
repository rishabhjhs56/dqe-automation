import os
import pandas as pd
import pytest



def get_latest_parquet():
    """Return the path to the sample parquet file"""
    # Use the sample files from data/sample_files
    table_name = "facility_name_min_time_spent_per_visit_date"
    
    # Try different possible paths to find the sample file
    possible_paths = [
        f"data/sample_files/{table_name}.parquet",
        f"PyTest DQ Framework/data/sample_files/{table_name}.parquet"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If no sample file is found, raise a helpful error
    raise ValueError(f"Sample file not found. Current directory: {os.getcwd()}")


@pytest.fixture(scope="module")
def target_data(parquet_reader):
    return parquet_reader.process(get_latest_parquet())


@pytest.fixture(scope="module")
def source_data(db_connection):
    query = """
    SELECT f.facility_name,
           DATE(v.visit_timestamp) AS visit_date,
           MIN(v.duration_minutes) AS avg_time_spent
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    GROUP BY f.facility_name, DATE(v.visit_timestamp)
    """
    return pd.read_sql(query, db_connection)


@pytest.mark.parquet_data
def test_not_empty(target_data, data_quality_library):
    data_quality_library.check_dataset_is_not_empty(target_data)


@pytest.mark.parquet_data
def test_count(source_data, target_data, data_quality_library):
    data_quality_library.check_count(source_data, target_data)


@pytest.mark.parquet_data
def test_nulls(target_data, data_quality_library):
    data_quality_library.check_nulls(target_data)


@pytest.mark.parquet_data
def test_duplicates(target_data, data_quality_library):
    data_quality_library.check_duplicates(target_data)
