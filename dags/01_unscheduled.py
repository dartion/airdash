import datetime as dt
from pathlib import Path
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


# Initialise DAG with scheduled_interval=None, where this DAG will be triggered manually from Airflow webserver
dag = DAG(
    dag_id="01_unscheduled",
    start_date=dt.datetime(2019, 1, 1),
    schedule_interval=None,
)

# Use start and end date to specify when the DAG starts executing and ends executing
# dag = DAG(
#  dag_id="03_with_end_date",
#  schedule_interval="@daily",
#  start_date=dt.datetime(year=2019, month=1, day=1),
#  end_date=dt.datetime(year=2019, month=1, day=5),
# )

# When a DAG is to be executed, for example every 3 days we could use timedelta as shown below
# dag = DAG(
#  dag_id="04_time_delta",
#  schedule_interval=dt.timedelta(days=3),
#  start_date=dt.datetime(year=2019, month=1, day=1),
#  end_date=dt.datetime(year=2019, month=1, day=5),
# )


fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data && "
        "curl -o /data/events.json "
        "https:/ /localhost:5000/events"
    ),
    dag=dag,
)

# Use execution_date to get the day when tag is executed
# fetch_events = BashOperator(
#  task_id="fetch_events",
#  bash_command=(
#  "mkdir -p /data && "
#  "curl -o /data/events.json "
#  "http:/ /localhost:5000/events?"
#  "start_date={{execution_date.strftime('%Y-%m-%d')}}"
#  "&end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
#  ),
#  dag=dag,
# )

# Jinja syntax can be used to specify parameters,ex: {{ ds }} represents datestring in YYYY-MM-DD
# fetch_events = BashOperator(
#  task_id="fetch_events",
#  bash_command=(
#  "mkdir -p /data && "
#  "curl -o /data/events.json "
#  "http:/ /localhost:5000/events?"
#  "start_date={{ds}}&"
#  "end_date={{next_ds}}"
#  ),
#  dag=dag,
# )

# Instead of fetching all the data to one file, doing it in daily seprate files with appropriate dates with avoid single
# point of failure
# fetch_events = BashOperator(
#  task_id="fetch_events",
#  bash_command=(
#  "mkdir -p /data/events && "
#  "curl -o /data/events/{{ds}}.json "
#  "http:/ /localhost:5000/events?"
#  "start_date={{ds}}&"
#  "end_date={{next_ds}}",
#  dag=dag,
# )
def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)

    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats,
        op_kwargs={
            "input_path": "/data/events.json",
            "output_path": "/data/stats.csv",
        },
        dag=dag,
    )


calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={
        "input_path": "/data/events.json",
        "output_path": "/data/stats.csv",
    },
    dag=dag,
)

# Calculate statistics for each file using **kwargs
# def _calculate_stats(**context):
#     """Calculates event statistics."""
#     input_path = context["templates_dict"]["input_path"]
#     output_path = context["templates_dict"]["output_path"]
#     Path(output_path).parent.mkdir(exist_ok=True)
#     events = pd.read_json(input_path)
#     stats = events.groupby(["date", "user"]).size().reset_index()
#     stats.to_csv(output_path, index=False)
#
# calculate_stats = PythonOperator(
#     task_id="calculate_stats",
#     python_callable=_calculate_stats,
#     templates_dict={
#     "input_path": "/data/events/{{ds}}.json",
#     "output_path": "/data/stats/{{ds}}.csv",
#     },
#     dag=dag,
# )
fetch_events >> calculate_stats
