from datetime import datetime
from datetime import timedelta
import os

from airflow import DAG
from airflow.providers.smtp.hooks.smtp import SmtpHook
from airflow.providers.standard.operators.bash import BashOperator

def gmail_fail_alert(context):
    ti = context["task_instance"]

    dag_id = ti.dag_id
    task_id = ti.task_id
    run_id = ti.run_id
    exception = context.get("exception")

    base_url = os.getenv(
        "AIRFLOW__WEBSERVER__BASE_URL",
        "http://localhost:8080",
    )

    log_url = (
        f"{base_url}/dags/{dag_id}"
        f"/grid?dag_run_id={run_id}&task_id={task_id}"
    )

    subject = f"🚨 Airflow Task Failed: {dag_id}.{task_id}"

    html_content = f"""
    <h2>Airflow Task Failed</h2>

    <ul>
        <li><b>DAG:</b> {dag_id}</li>
        <li><b>Task:</b> {task_id}</li>
        <li><b>Run ID:</b> {run_id}</li>
        <li><b>Error:</b> {exception}</li>
    </ul>

    <p>
        <a href="{log_url}">
            View Logs
        </a>
    </p>
    """

    hook = SmtpHook(smtp_conn_id="gmail_connection")

    hook.get_conn()

    hook.send_email_smtp(
        to="alert_recipient@example.com",
        subject=subject,
        html_content=html_content,
    )

PROJECT_DIR = "/home/yoda/code/dataeng/project/yellow_trip"
VENV = f"{PROJECT_DIR}/.venv/bin"

default_args = {
    "owner": "yoda",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": gmail_fail_alert,
}


with DAG(
    dag_id="yellow_trip_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["yellow_trip"],
) as dag:
    ingest = BashOperator(
        task_id="ingest",
        bash_command=(
            f"{VENV}/python "
            f"{PROJECT_DIR}/ingestion/ingest.py"
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"cd {PROJECT_DIR}/yellow_trip && "
            f"{VENV}/dbt run"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="exit 1",
    )

    ingest >> dbt_run >> dbt_test
