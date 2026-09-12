from pathlib import Path
from airflow.configuration import conf

import pendulum
from airflow.sdk import CronDataIntervalTimetable, chain, dag, task, task_group

start_date = pendulum.datetime(2026, 1, 1, tz='UTC')

DAGS_FOLDER = Path(conf.get('core', 'dags_folder'))
# DAGS_DIR = Path(__file__).resolve().parent
ORCHESTRATION_DIR = (DAGS_FOLDER / '..').resolve()
INGESTION_DIR = (DAGS_FOLDER / '..' /'..' / 'ingestion').resolve()
TRANSFORMATION_DIR = (DAGS_FOLDER / '..' / '..' / 'transformation').resolve()
INGESTION_DATA_DIR = (INGESTION_DIR / 'data').resolve()

VENV = (DAGS_FOLDER / '..' / '..' / '.venv' / 'bin').resolve()

default_args = {
    'retries': 2,
    'retry_delay':  pendulum.duration(minutes=1),
    'retry_exponential_backoff': True,
}

@dag(
    dag_id="yellow_trip_orchestration",
    description="Data workflow that represents data ingestion, loading and transformation on NYC Yellow Taxi Trip Data",
    start_date=start_date,
    schedule=CronDataIntervalTimetable('0 0 1 * *', timezone='UTC'),
    catchup=False,
    default_args=default_args,
    doc_md="""
### Yellow Trip
Orchestrates the NYC Yellow Taxi Trip Data pipeline.

1. **Schedule:** Monthly, at `00:00 UTC` on the 1st day of the month.  
2. **Data interval:** The previous month.  
3. **Catchup:** Disabled.  
4. **Max active runs:** `1`.

#### Workflow
1. **Ingest** -> Downloads/ingests the Yellow Taxi data for the data interval.
2. **Seed** -> Runs `dbt seed` to load seed data.
3. **Transform** -> Runs:
   - `dbt run`
   - `dbt test`

Ingestion and seeding run in parallel. Transformation starts after both complete.
""",
    max_active_runs=1,
    tags=['projects'],
)
def yellow_trip():
    @task.bash(
        cwd=str(INGESTION_DIR), 
        execution_timeout=pendulum.duration(minutes=5)
    ) 
    def ingest() -> str:
        return f"{VENV}/python ingest_month.py --date {{{{ data_interval_start.strftime('%Y-%m-%d') }}}}"

    @task.bash(
        cwd=str(TRANSFORMATION_DIR), 
        execution_timeout=pendulum.duration(minutes=5)
    )
    def dbt_seed():
        return f'{VENV}/dbt seed'

    @task_group(
        group_id='transform'
    )
    def transform():

        @task.bash(
            cwd=str(TRANSFORMATION_DIR), 
            execution_timeout=pendulum.duration(minutes=5)
        )
        def dbt_run():
            return f'{VENV}/dbt run'

        @task.bash(
            cwd=str(TRANSFORMATION_DIR), 
            execution_timeout=pendulum.duration(minutes=5)
        )
        def dbt_test():
            return f'{VENV}/dbt test'


        dbt_run() >> dbt_test()

    [ingest(), dbt_seed()] >> transform()

yellow_trip()
