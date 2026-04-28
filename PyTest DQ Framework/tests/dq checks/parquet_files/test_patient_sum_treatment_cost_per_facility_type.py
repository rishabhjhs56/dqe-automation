# tests/dq_checks/parquet_files/test_patient_sum_treatment_cost_per_facility_type.py

import os
import pytest
import pandas as pd


def get_parquet_path(dataset_name):
    path1 = f"output/parquet/{dataset_name}"
    path2 = f"PyTest DQ Framework/output/parquet/{dataset_name}"

    if os.path.exists(path1):
        return path1

    if os.path.exists(path2):
        return path2

    raise FileNotFoundError(f"{dataset_name} folder not found")


@pytest.fixture(scope="module")
def target_data(parquet_reader):
    target_path = get_parquet_path(
        "patient_sum_treatment_cost_per_facility_type"
    )
    return parquet_reader.process(target_path)


@pytest.fixture(scope="module")
def source_data(db_connection):
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


@pytest.mark.parquet_data
def test_negative_values(target_data):
    assert (target_data["sum_treatment_cost"] >= 0).all(), \
        "Negative treatment cost found"
