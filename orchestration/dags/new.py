from airflow.sdk import dag, task, chain, task_group
import os

import pendulum

now = pendulum.datetime(2026, 1, 1)

ORCHESTRATION_DIR = os.getenv("AIRFLOW_HOME")

INGESTION_DIR = f"{ORCHESTRATION_DIR}/../ingestion"
TRANSFORMATION_DIR = f"{ORCHESTRATION_DIR}/../transformation"

VENV = f'{ORCHESTRATION_DIR}/../.venv/bin'

@dag(
    dag_id="yellow_trip",
    description="sigma dag",
    start_date=now,
    tags="yoda"
)
def yellow_trip():
    @task.bash
    def pwd() -> str:
        return 'pwd'

    @task.bash
    def create_duckdb() -> str:
        return f'cd {ORCHESTRATION_DIR}/../data && duckdb taxi.duckdb ""'

    @task.bash
    def ingest() -> str:
        return f'cd {INGESTION_DIR} && {VENV}/python ingest.py'

    @task_group(group_id='transform')
    def transform():
        @task.bash
        def dbt_seed():
            return f'cd {TRANSFORMATION_DIR} && {VENV}/dbt seed'

        @task.bash
        def dbt_run():
            return f'cd {TRANSFORMATION_DIR} && {VENV}/dbt run'

        @task.bash
        def dbt_test():
            return f'cd {TRANSFORMATION_DIR} && {VENV}/dbt test'

        chain(dbt_seed(), dbt_run(), dbt_test())

    chain(pwd(), create_duckdb(), pwd(), ingest(), transform())

yellow_trip()
