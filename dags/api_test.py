import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

'''Before running the curl commmand, check auth_backend value set in airflow.cfg to be 
auth_backend = airflow.api.auth.backend.basic_auth

and then run the command from terminal 
 curl -u airflow:airflow -X POST "http://localhost:8080/api/v1/dags/print_dag_run_conf/dagRuns" -H "Content-Type: application/json" -d '{"conf": {"supermarket": 1}}'

to get the output
{
  "conf": {
    "supermarket": 1
  },
  "dag_id": "print_dag_run_conf",
  "dag_run_id": "manual__2021-07-04T04:06:46.574337+00:00",
  "end_date": null,
  "execution_date": "2021-07-04T04:06:46.574337+00:00",
  "external_trigger": true,
  "start_date": "2021-07-04T04:06:46.577570+00:00",
  "state": "running"
} 
'''
dag = DAG(
    dag_id="print_dag_run_conf",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
)

def print_conf(**context): print(context["dag_run"].conf)

process = PythonOperator(
        task_id="process",
        python_callable=print_conf,
        dag=dag,
)