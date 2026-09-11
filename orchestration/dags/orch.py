from airflow.sdk import CronDataIntervalTimetable, chain, dag, task, task_group
import os
from pathlib import Path

import pendulum

# utc aware

start_date = pendulum.datetime(2026, 1, 1, tz='UTC')

ORCHESTRATION_DIR = Path(os.environ["AIRFLOW_HOME"])

INGESTION_DIR = (ORCHESTRATION_DIR  / '..' / 'ingestion').resolve()
TRANSFORMATION_DIR = (ORCHESTRATION_DIR / '..' / 'transformation').resolve()

VENV = (ORCHESTRATION_DIR / '..' / '.venv' / 'bin').resolve()

default_args = {
    'retries': 2,
    'retry_delay':  pendulum.duration(minutes=1),
    'retry_exponential_backoff': True,
}

@dag(
    dag_id="yellow_trip_orchestration",
    description="sigma dag",
    start_date=start_date,
    schedule=CronDataIntervalTimetable('0 0 1 * *', timezone='UTC'),
    catchup=False,
    # default_args=default_args,
    doc_md="""
        based dag
    """,
    tags=['projects'],
)
def yellow_trip():
    @task.bash(cwd=str(ORCHESTRATION_DIR))
    def create_duckdb() -> str:
        return 'duckdb taxi.duckdb ""'

    @task.bash(cwd=str(INGESTION_DIR))
    def ingest() -> str:
        return f"{VENV}/python ingest_month.py --date {{{{ data_interval_start.strftime( '%Y-%m-%d' ) }}}}"

    @task_group(group_id='transform')
    def transform():
        @task.bash(cwd=str(TRANSFORMATION_DIR), execution_timeout=pendulum.duration(minutes=30))
        def dbt_seed():
            return f'{VENV}/dbt seed'

        @task.bash(cwd=str(TRANSFORMATION_DIR), execution_timeout=pendulum.duration(minutes=30))
        def dbt_run():
            return f'{VENV}/dbt run'

        @task.bash(cwd=str(TRANSFORMATION_DIR), execution_timeout=pendulum.duration(minutes=30))
        def dbt_test():
            return f'{VENV}/dbt test'

        chain(dbt_seed(), dbt_run(), dbt_test())

    chain(create_duckdb(), ingest(), transform())

yellow_trip()
