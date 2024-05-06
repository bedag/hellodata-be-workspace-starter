#### Following configuration (the "hd_env") makes it possible to load the current runtime environment into the local dag.
import sys
import os
current_file = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file)
sys.path.append(current_directory)
# load the environment
from hd_env import common_k8s_pod_operator_params, workspace_name
#### < end hd_env config


from pendulum import datetime
from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s
import os


default_args = {
    "owner": "airflow",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    # "retry_delay": duration(minutes=5),
}


with DAG(
    dag_id="run_boiler_example",
    schedule="@once",
    default_args=default_args,
    description="Boiler Plate for running a hello data workspace in airflow",
    tags=[workspace_name],
) as dag:
    KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="airflow-running-dagster-workspace",
        task_id="run_duckdb_query",
        # please add/overwrite your command here
        arguments=[
            "python query_duckdb.py && echo 'Query executed successfully'",  # add your command here
        ],
    )
