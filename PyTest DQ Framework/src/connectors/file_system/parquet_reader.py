import pandas as pd

class ParquetReader:

    def __init__(self):
        pass

    def process(self, file_path):
        try:
            return pd.read_parquet(file_path, engine="pyarrow")
        except Exception as e:
            raise RuntimeError(f"Failed to read parquet file: {e}")
            
