import pandas as pd

class ParquetReader:
    def __init__(self):
        pass

    def process(self, file_path):
        # Reads a Parquet file and returns a DataFrame
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            raise RuntimeError(f"Failed to read parquet file: {e}")
