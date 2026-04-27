import os
from src.connectors.postgres.psycopg2_wrapper import psycopg2


class PostgresConnectorContextManager:

    def __init__(
        self,
        db_host=None,
        db_port=None,
        db_name=None,
        db_user=None,
        db_password=None
    ):
        self.db_host = db_host or os.getenv("DB_HOST", "localhost")
        self.db_port = db_port or os.getenv("DB_PORT", "5432")
        self.db_name = db_name or os.getenv("DB_NAME", "mydatabase")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
