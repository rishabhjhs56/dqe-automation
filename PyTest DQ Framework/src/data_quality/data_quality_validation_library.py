import pandas as pd


class DataQualityLibrary:

    @staticmethod
    def check_row_count(df):
        assert len(df) > 0, "DataFrame is empty"

    @staticmethod
    def check_nulls(df):
        null_counts = df.isnull().sum()
        assert null_counts.sum() == 0, f"Null values found:\n{null_counts}"

    @staticmethod
    def check_duplicates(df):
        dup_count = df.duplicated().sum()
        assert dup_count == 0, f"Duplicate rows found: {dup_count}"

    @staticmethod
    def check_columns_exist(df, expected_columns):
        missing = [col for col in expected_columns if col not in df.columns]
        assert not missing, f"Missing columns: {missing}"

    @staticmethod
    def check_data_types(df, expected_types):
        for col, dtype in expected_types.items():
            assert col in df.columns, f"{col} not found"
            assert str(df[col].dtype) == dtype, f"{col} datatype mismatch"
