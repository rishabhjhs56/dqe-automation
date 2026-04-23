import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent

csv_file = base / "employee.csv"
parquet_file = base / "employees.parquet"

df = pd.read_csv(csv_file)
df.to_parquet(parquet_file, index=False, engine="pyarrow")

print("employees.parquet created successfully")