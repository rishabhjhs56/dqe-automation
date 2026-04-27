import pandas as pd
from pathlib import Path

# Get current script directory
base = Path(file).resolve().parent

csv_file = base / "employee.csv"
parquet_file = base / "employees.parquet"

# CSV → Parquet
df = pd.read_csv(csv_file)
df.to_parquet(parquet_file, index=False, engine="pyarrow")

print("employees.parquet created successfully")

# -------------------------------
# Parquet file 1
# -------------------------------
pqt_data = [
    {"facility_name": "MayoClinic", "visit_date": "2023-05-01", "min_time_spent": 30},
    {"facility_name": "City Hospital", "visit_date": "2023-05-02", "min_time_spent": 45},
]

pd.DataFrame(pqt_data).to_parquet(
    base / "facility_name_min_time_spent_per_visit_date.parquet",
    index=False,
    engine="pyarrow",
)

# -------------------------------
# Parquet file 2
# -------------------------------
pqt_data2 = [
    {"facility_type": "Hospital", "visit_date": "2023-05-02", "avg_time_spent": 24.00}
]

pd.DataFrame(pqt_data2).to_parquet(
    base / "facility_type_avg_time_spent_per_visit_date.parquet",
    index=False,
    engine="pyarrow",
)

# -------------------------------
# Parquet file 3
# -------------------------------
pqt_data3 = [
    {"facility_type": "Clinic", "patient_sum_treatment_cost": 150.00},
    {"facility_type": "Hospital", "patient_sum_treatment_cost": 200.00},
]

pd.DataFrame(pqt_data3).to_parquet(
    base / "patient_sum_treatment_cost_per_facility_type.parquet",
    index=False,
    engine="pyarrow",
)