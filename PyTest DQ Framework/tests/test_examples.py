"""
Description: Data Quality checks for Source vs Target parquet validation
Requirement(s): TICKET-1234
Author(s): Rishabh Gupta
"""

import pytest


# ---------------------------------------------------
# Source Data Fixture (Postgres)
# ---------------------------------------------------
@pytest.fixture(scope="module")
def source_data(db_connection):
    source_query = """
        SELECT *
        FROM employees
    """
    data = db_connection.get_data_sql(source_query)
    return data


# ---------------------------------------------------
# Target Data Fixture (Parquet File)
# ---------------------------------------------------
@pytest.fixture(scope="module")
def target_data(parquet_reader):
    target_path = "target_path = "PyTest DQ Framework/data/sample_files/employees.parquet"
    data = parquet_reader.process(target_path)
    return data


# ---------------------------------------------------
# Test 1 - Target dataset should not be empty
# ---------------------------------------------------
@pytest.mark.parquet_data
def test_check_dataset_is_not_empty(target_data, dq):
    dq.check_dataset_is_not_empty(target_data)


# ---------------------------------------------------
# Test 2 - Source vs Target row count match
# ---------------------------------------------------
@pytest.mark.parquet_data
def test_check_count(source_data, target_data, dq):
    dq.check_count(source_data, target_data)
