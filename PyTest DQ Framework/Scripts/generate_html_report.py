import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load the Parquet file
df = pd.read_parquet("facility_type_avg_time_spent_per_visit_date.parquet")

# Filter for last 7 days
today = datetime.today().date()
last_7_days = [(today - timedelta(days=i)) for i in range(7)]
df['visit_date'] = pd.to_datetime(df['visit_date']).dt.date
df_last_week = df[df['visit_date'].isin(last_7_days)]

# Generate Table HTML
table_html = df_last_week.to_html(index=False)

# Generate Doughnut Chart
avg_time_by_type = df_last_week.groupby('facility_type')['avg_time_spent'].mean()
fig = go.Figure(data=[go.Pie(labels=avg_time_by_type.index, values=avg_time_by_type.values, hole=.4)])
fig.update_layout(title_text="Min average time spent by Facility Type for the last week")
doughnut_html = fig.to_html(full_html=False)

# Combine into one HTML file
html_report = f"""
<html>
<head>
    <title>Facility Type Data Quality Report - Last 7 Days</title>
</head>
<body>
    <h2>Table: Last week loaded data</h2>
    {table_html}
    <h2>Doughnut: Min average time spent by Facility Type for the last week</h2>
    {doughnut_html}
</body>
</html>
"""

with open("html_report/facility_type_avg_time_spent_per_visit_date_report.html", "w") as f:
    f.write(html_report)

print("HTML report generated: html_report/facility_type_avg_time_spent_per_visit_date_report.html")
