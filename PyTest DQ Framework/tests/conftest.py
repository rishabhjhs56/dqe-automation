import pytest
from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.file_system.parquet_reader import ParquetReader


def pytest_addoption(parser):
    parser.addoption("--db_host", action="store", default="localhost", help="Database host")
    parser.addoption("--db_port", action="store", default="5432", help="Database port")
    parser.addoption("--db_name", action="store", default="mydatabase", help="Database name")
    parser.addoption("--db_user", action="store", help="Database user")
    parser.addoption("--db_password", action="store", help="Database password")


def pytest_configure(config):
    required_options = ["db_user", "db_password"]
    for opt in required_options:
        if not config.getoption(f"--{opt}"):
            raise pytest.
UsageError(f"Missing required option: --{opt}")


@pytest.fixture(scope="session")
def db_connection(request):
    host = request.config.getoption("--db_host")
    port = request.config.getoption("--db_port")
    dbname = request.config.getoption("--db_name")
    user = request.config.getoption("--db_user")
    password = request.config.getoption("--db_password")

    try:
        with PostgresConnectorContextManager(
            db_host=host,
            db_port=port,
            db_name=dbname,
            db_user=user,
            db_password=password
        ) as conn:
            yield conn
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


@pytest.fixture(scope="session")
def dq():
    return DataQualityLibrary()


@pytest.fixture(scope="session")
def parquet_reader():
    return ParquetReader()
