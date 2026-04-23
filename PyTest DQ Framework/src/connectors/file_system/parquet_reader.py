import pandas as pd

class ParquetReader:

    def process(self, file_path):
        df = pd.read_parquet(file_path)
        return df
