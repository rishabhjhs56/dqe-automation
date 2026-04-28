import pyarrow.dataset as ds
import pandas as pd

# ✅ Input folder (partitioned dataset)
input_path = "/Users/rishabhgupta/Documents/dqe-automation/PyTest DQ Framework/output/parquet/patient_sum_treatment_cost_per_facility_type"

# ✅ Output file
output_file = "parquet_data/patient_sum_treatment_cost_per_facility_type.parquet"

# 🔥 Read full dataset (handles partitions automatically)
dataset = ds.dataset(input_path, format="parquet")

# Convert to table
table = dataset.to_table()

# Convert to pandas
df = table.to_pandas()

# Optional: convert all columns to string (safe comparison)
df = df.astype(str)

# Save as single parquet file
df.to_parquet(output_file, index=False)

print("✅ Merged parquet created:", output_file)