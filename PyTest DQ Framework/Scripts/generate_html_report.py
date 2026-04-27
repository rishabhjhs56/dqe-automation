import os
import glob
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta


# ---------------------------------------------------
# Find latest parquet output folder
# ---------------------------------------------------
def get_latest_parquet_folder():
    folders = sorted(
        glob.glob("PyTest DQ Framework/output/*/parquet")
    )

    if not folders:
        raise FileNotFoundError(
            "No parquet output folder found."
        )

    return folders[-1]


# ---------------------------------------------------
# Create report output path
# ---------------------------------------------------
def get_report_folder():
    report_dir = "PyTest DQ Framework/html_report"
    os.makedirs(report_dir, exist_ok=True)
    return report_dir


# ---------------------------------------------------
# Load parquet data
# ---------------------------------------------------
latest_folder = get_latest_parquet_folder()

file_path = os.path.join(
    latest_folder,
    "facility_type_avg_time_spent_per_visit_date"
)

df = pd.read_parquet(file_path)


# ---------------------------------------------------
# Prepare Date Column
# ---------------------------------------------------
df["visit_date"] = pd.to_datetime(df["visit_date"]).dt.date

today = datetime.today().date()
last_7_days = [
    today - timedelta(days=i)
    for i in range(7)
]

df_last_week = df[
    df["visit_date"].isin(last_7_days)
].copy()


# ---------------------------------------------------
# If no data found for last week use latest 7 rows
# ---------------------------------------------------
if df_last_week.empty:
    df_last_week = df.sort_values(
        by="visit_date",
        ascending=False
    ).head(7)


# ---------------------------------------------------
# Table HTML
# ---------------------------------------------------
table_html = df_last_week.to_html(
    index=False,
    classes="styled-table",
    border=0
)


# ---------------------------------------------------
# Doughnut Chart
# ---------------------------------------------------
chart_data = (
    df_last_week.groupby("facility_type")["avg_time_spent"]
    .min()
    .reset_index()
)

fig = go.Figure(
    data=[
        go.Pie(
            labels=chart_data["facility_type"],
            values=chart_data["avg_time_spent"],
            hole=0.45
        )
    ]
)

fig.update_layout(
    title="Minimum Average Time Spent by Facility Type (Last 7 Days)",
    height=500
)

chart_html = fig.to_html(
    full_html=False,
    include_plotlyjs="cdn"
)


# ---------------------------------------------------
# Final HTML Template
# ---------------------------------------------------
run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_report = f"""
<html>
<head>
<title>Facility Type Dashboard</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    background-color: #f8f9fa;
}}

h1 {{
    color: #222;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 25px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.styled-table {{
    border-collapse: collapse;
    width: 100%;
}}

.styled-table th {{
    background: #343a40;
    color: white;
    padding: 10px;
}}

.styled-table td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}

.footer {{
    margin-top: 30px;
    color: gray;
    font-size: 12px;
}}
</style>

</head>

<body>

<h1>Data Quality BI Dashboard</h1>

<div class="card">
<b>Source File:</b> facility_type_avg_time_spent_per_visit_date<br>
<b>Generated At:</b> {run_time}<br>
<b>Parquet Folder:</b> {latest_folder}
</div>

<div class="card">
<h2>Last 7 Days Data</h2>
{table_html}
</div>

<div class="card">
<h2>Doughnut Chart</h2>
{chart_html}
</div>

<div class="footer">
Generated automatically by Jenkins Pipeline
</div>

</body>
</html>
"""


# ---------------------------------------------------
# Save Report
# ---------------------------------------------------
report_folder = get_report_folder()

report_path = os.path.join(
    report_folder,
    "facility_type_dashboard.html"
)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(html_report)

print(f"HTML report generated: {report_path}")
