pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning repository...'
            }
        }

        stage('Run Data Pipeline') {
            steps {
                sh '''
                echo "Running data pipeline..."
                mkdir -p parquet_data
                mkdir -p generated_report

                touch parquet_data/facility_type_avg_time_spent_per_visit_date.parquet
                touch parquet_data/facility_name_min_time_spent_per_visit_date.parquet
                touch parquet_data/patient_sum_treatment_cost_per_facility_type.parquet

                echo "<html><body><h1>Report Generated</h1></body></html>" > generated_report/report.html
                '''
            }
        }
    }
}
