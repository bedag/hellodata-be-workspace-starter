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
    dag_id="run_showcase_boiler_example",
    schedule="@once",
    default_args=default_args,
    description="Showcase to run Airflow and dbt on hello data workspace in airflow",
    tags=[workspace_name],
) as dag:
    data_download = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="data-download",
        task_id="data_download",
        arguments=[
            "python dags-functions/showcase.py --data_download && echo 'download successfully'"
        ],
    )

    create_tables = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="create-tables",
        task_id="create_tables",
        arguments=[
            "python dags-functions/showcase.py --create_tables && echo 'created tables successfully'"
        ],
    )

    insert_data = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="insert-data",
        task_id="insert_data",
        arguments=[
            "python dags-functions/showcase.py --insert_data && echo 'insert data successfully'"
        ],
    )

    dbt_run = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="dbt-run",
        task_id="dbt_run",
        arguments=[
            "cd /usr/src/app/dbt/ && dbt run && echo 'dbt run successfully' && dbt docs generate --target-path /usr/src/app/dbt-docs && echo 'dbt docs generate successfully'",
        ],
    )

    # Defining task dependencies
    (
        data_download
        >> create_tables
        >> insert_data
        >> dbt_run
        # >> dbt_docs_serve
    )
