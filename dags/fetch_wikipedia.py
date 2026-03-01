from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="fetch_wikipedia_page",
    description="Fetch a Wikipedia page using curl",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    default_args=default_args,
) as dag:

    fetch_page = BashOperator(
        task_id="curl_lebron_james",
        bash_command=(
            "curl -L https://simple.wikipedia.org/wiki/LeBron_James "
            "> /opt/airflow/logs/lebron_page.html"
        ),
    )
