import os
import glob
import pandas as pd
import plotly.express as px

# Base output folder
base_path = "PyTest DQ Framework/output"

# Latest dated folder pick karega automatically
latest_folder = sorted(glob.glob(f"{base_path}/*"))[-1]

# Exact parquet path
parquet_path = os.path.join(
    latest_folder,
    "parquet",
    "facility_type_avg_time_spent_per_visit_date"
)

# Read parquet (partitioned folder bhi read ho jayega)
df = pd.read_parquet(parquet_path)

# Chart
fig = px.pie(
    df,
    names="facility_type",
    values="avg_time_spent",
    hole=0.5,
    title="Average Time Spent by Facility Type"
)

# Report save path
report_path = os.path.join(
    latest_folder,
    "html_report",
    "report.html"
)

os.makedirs(os.path.dirname(report_path), exist_ok=True)

fig.write_html(report_path)

print(f"HTML Report Generated: {report_path}")
