from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def step(msg):
    print(msg)

with DAG(
    dag_id="sequential_workflow",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="extract",
        python_callable=lambda: step("Extracting data..."),
    )

    t2 = PythonOperator(
        task_id="transform",
        python_callable=lambda: step("Transforming data..."),
    )

    t3 = PythonOperator(
        task_id="load",
        python_callable=lambda: step("Loading data..."),
    )

    t1 >> t2 >> t3
