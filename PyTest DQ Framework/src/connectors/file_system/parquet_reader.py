import pandas as pd
import pytest


class ParquetReader:
    def parquet_reader(request):
        try:
            reader = ParquetReader()
            yield reader
        except Exception as e:
            pytest.fail(f"Failed to initialize ParquetReader: {e}")
        finally:
            del reader
