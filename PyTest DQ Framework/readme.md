# Data Quality Automation Framework

## Overview
Validates transformation of data from Postgres to Parquet files.

## Setup
- Clone repo
- Configure Postgres
- Run Jenkins pipeline

## Data Generation
- See `data_generation/generate_data.sql`

## Transformation
- See `transformation/transform_to_parquet.py`

## Testing
- See `tests/test_examples.py`

## CI/CD
- See `Jenkinsfile`

## Deliverables
- PyTest HTML report in `html_report/`
- Transformation issues summary in `docs/summary_of_issues.md`
- Screenshots in `assets/`

## Revision History
- See Document Control section

## Acknowledgments
- See Document Control section
