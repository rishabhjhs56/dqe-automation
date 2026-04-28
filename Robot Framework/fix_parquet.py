import pyarrow.parquet as pq
import pandas as pd

# Input problematic file
input_file = "/Users/rishabhgupta/Documents/dqe-automation/PyTest DQ Framework/output/parquet/facility_type_avg_time_spent_per_visit_date/visit_year_month=2026-04/facility_type_avg_time_spent_per_visit_date.parquet"

# Output clean file
output_file = "parquet_data/facility_type_avg_timepatient_sum_treatment_cost_per_facility_type_spent_per_visit_date.parquet"

# Read safely
table = pq.read_table(input_file)

# Convert to pandas safely
df = table.to_pandas()

# 🔥 Convert everything to string (remove schema issues)
df = df.astype(str)

# Save clean parquet
df.to_parquet(output_file, index=False)

print("✅ Clean parquet created:", output_file)