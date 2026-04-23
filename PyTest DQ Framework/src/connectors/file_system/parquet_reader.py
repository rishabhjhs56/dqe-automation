import pandas as pd


class ParquetReader:

    @staticmethod
    def read(file_path):
        return pd.read_parquet(file_path)

    @staticmethod
    def load(file_path):
        return pd.read_parquet(file_path)
