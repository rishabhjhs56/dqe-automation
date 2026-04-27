import os
import glob
import pandas as pd
import plotly.express as px

base_path = "PyTest DQ Framework/output"
latest_folder = sorted(glob.glob(f"{base_path}/*"))[-1]

parquet_path = os.path.join(
    latest_folder,
    "parquet",
    "facility_type_avg_time_spent_per_visit_date"
)

df = pd.read_parquet(parquet_path)

df["visit_date"] = pd.to_datetime(df["visit_date"])
df = df.sort_values("visit_date", ascending=False).head(7)

fig = px.pie(
    df,
    names="facility_type",
    values="avg_time_spent",
    hole=0.55,
    title="Average Time Spent by Facility Type"
)

chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

table_html = df[[
    "facility_type",
    "visit_date",
    "avg_time_spent"
]].to_html(index=False)

html = f"""
<html>
<head>
<title>Facility Dashboard</title>
<style>
body {{
font-family: Arial;
margin:40px;
background:#f8f9fa;
}}
.container {{
background:white;
padding:30px;
border-radius:10px;
box-shadow:0 0 10px #ddd;
}}
h1,h2 {{
text-align:center;
}}
table {{
width:100%;
border-collapse:collapse;
margin-top:20px;
}}
th,td {{
padding:12px;
border:1px solid #ddd;
text-align:center;
}}
th {{
background:#343a40;
color:white;
}}
.chart {{
margin-top:40px;
}}
</style>
</head>

<body>
<div class="container">

<h1>Data Quality BI Dashboard</h1>

<h2>Last 7 Days Data</h2>
{table_html}

<div class="chart">
{chart_html}
</div>

</div>
</body>
</html>
"""

output_dir = "PyTest DQ Framework/html_report"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/facility_type_dashboard.html", "w") as f:
    f.write(html)

print("Dashboard created")
