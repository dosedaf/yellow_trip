from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_DIR = "/home/yoda/code/dataeng/project/yellow_trip"
VENV = f"{PROJECT_DIR}/.venv/bin"

with DAG(
    dag_id="yellow_trip_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id="ingest",
        bash_command=f"{VENV}/python {PROJECT_DIR}/ingestion/ingest.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT_DIR}/yellow_trip && {VENV}/dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT_DIR}/yellow_trip && {VENV}/dbt test",
    )

    ingest >> dbt_run >> dbt_test
