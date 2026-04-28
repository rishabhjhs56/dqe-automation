# tests/dq_checks/parquet_files/test_facility_type_avg_time_spent_per_visit_date.py

import os
import pytest
import pandas as pd


def get_parquet_path(dataset_name):
    path1 = f"output/{dataset_name}"
    path2 = f"PyTest DQ Framework/output/{dataset_name}"

    if os.path.exists(path1):
        return path1

    if os.path.exists(path2):
        return path2

    raise FileNotFoundError(f"{dataset_name} folder not found")


@pytest.fixture(scope="module")
def target_data(parquet_reader):
    target_path = get_parquet_path(
        "facility_type_avg_time_spent_per_visit_date"
    )
    return parquet_reader.process(target_path)


@pytest.fixture(scope="module")
def source_data(db_connection):
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
