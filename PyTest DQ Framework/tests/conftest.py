import os
import pytest

from src.connectors.postgres.postgres_connector import PostgresConnectorContextManager
from src.data_quality.data_quality_validation_library import DataQualityLibrary
from src.connectors.file_system.parquet_reader import ParquetReader


def pytest_addoption(parser):
    parser.addoption(
        "--db_host",
        action="store",
        default=os.getenv("DB_HOST", "localhost"),
        help="Database host"
    )
    parser.addoption(
        "--db_port",
        action="store",
        default=os.getenv("DB_PORT", "5432"),
        help="Database port"
    )
    parser.addoption(
        "--db_name",
        action="store",
        default=os.getenv("DB_NAME", "mydatabase"),
        help="Database name"
    )
    parser.addoption(
        "--db_user",
        action="store",
        default=os.getenv("DB_USER"),
        help="Database user"
    )
    parser.addoption(
        "--db_password",
        action="store",
        default=os.getenv("DB_PASSWORD"),
        help="Database password"
    )


def pytest_configure(config):
    required_options = ["db_user", "db_password"]

    for opt in required_options:
        if not config.getoption(opt):
            raise pytest.UsageError(
                f"Missing required option: --{opt}"
            )


@pytest.fixture(scope="session")
def db_connection(request):
    try:
        with PostgresConnectorContextManager(
            db_host=request.config.getoption("db_host"),
            db_port=request.config.getoption("db_port"),
            db_name=request.config.getoption("db_name"),
            db_user=request.config.getoption("db_user"),
            db_password=request.config.getoption("db_password")
        ) as conn:
            yield conn

    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


@pytest.fixture(scope="session")
def parquet_reader():
    try:
        reader = ParquetReader()
        yield reader

    except Exception as e:
        pytest.fail(f"Failed to initialize ParquetReader: {e}")


@pytest.fixture(scope="session")
def data_quality_library():
    try:
        dq_lib = DataQualityLibrary()
        yield dq_lib

    except Exception as e:
        pytest.fail(f"Failed to initialize DataQualityLibrary: {e}")
