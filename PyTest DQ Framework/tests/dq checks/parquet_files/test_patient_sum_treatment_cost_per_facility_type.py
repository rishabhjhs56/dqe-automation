import glob
import pandas as pd
import pytest


def get_latest_parquet():
    folders = sorted(glob.glob("PyTest DQ Framework/output/*/parquet"))
    latest = folders[-1]
    return f"{latest}/patient_sum_treatment_cost_per_facility_type"


@pytest.fixture(scope="module")
def target_data(parquet_reader):
    return parquet_reader.process(get_latest_parquet())


@pytest.fixture(scope="module")
def source_data(db_connection):
    query = """
    SELECT f.facility_type,
           CONCAT(p.first_name,' ',p.last_name) AS full_name,
           SUM(v.treatment_cost) AS sum_treatment_cost
    FROM visits v
    JOIN facilities f ON v.facility_id = f.id
    JOIN patients p ON v.patient_id = p.id
    GROUP BY f.facility_type, p.first_name, p.last_name
    """
    return pd.read_sql(query, db_connection)


@pytest.mark.parquet_data
def test_negative(target_data):
    assert (target_data["sum_treatment_cost"] >= 0).all()
