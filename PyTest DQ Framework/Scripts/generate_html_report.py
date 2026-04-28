import os
from pathlib import Path

import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Base Project Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
PARQUET_DIR = OUTPUT_DIR / "parquet"
REPORT_DIR = BASE_DIR / "html_report"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Read Parquet Data
# --------------------------------------------------
parquet_path = PARQUET_DIR / "facility_type_avg_time_spent_per_visit_date"

if not parquet_path.exists():
    raise FileNotFoundError(
        f"Parquet path not found: {parquet_path}"
    )

df = pd.read_parquet(parquet_path)

if df.empty:
    raise ValueError("No data found in parquet file.")


# --------------------------------------------------
# Data Preparation
# --------------------------------------------------
df["visit_date"] = pd.to_datetime(df["visit_date"])
df = df.sort_values("visit_date", ascending=False).head(7)

display_df = df[
    ["facility_type", "visit_date", "avg_time_spent"]
].copy()

display_df["visit_date"] = display_df["visit_date"].dt.strftime("%Y-%m-%d")


# --------------------------------------------------
# Create Pie Chart
# --------------------------------------------------
fig = px.pie(
    df,
    names="facility_type",
    values="avg_time_spent",
    hole=0.55,
    title="Average Time Spent by Facility Type"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    title_x=0.5,
    template="plotly_white",
    height=500
)

chart_html = fig.to_html(
    full_html=False,
    include_plotlyjs="cdn"
)


# --------------------------------------------------
# HTML Table
# --------------------------------------------------
table_html = display_df.to_html(
    index=False,
    classes="table",
    border=0
)


# --------------------------------------------------
# Final HTML
# --------------------------------------------------
html = f"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Facility Dashboard</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 30px;
    background: #f4f6f8;
}}

.container {{
    max-width: 1200px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

h1 {{
    text-align: center;
    color: #222;
}}

h2 {{
    margin-top: 40px;
    text-align: center;
    color: #444;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th, td {{
    padding: 12px;
    border: 1px solid #ddd;
    text-align: center;
}}

th {{
    background: #343a40;
    color: white;
}}

tr:nth-child(even) {{
    background: #f8f9fa;
}}

.chart {{
    margin-top: 40px;
}}
</style>
</head>

<body>

<div class="container">

<h1>Data Quality BI Dashboard</h1>

<h2>Last 7 Days Facility Data</h2>
{table_html}

<div class="chart">
{chart_html}
</div>

</div>

</body>
</html>
"""


# --------------------------------------------------
# Save HTML File
# --------------------------------------------------
output_file = REPORT_DIR / "facility_type_dashboard.html"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard created successfully: {output_file}")
