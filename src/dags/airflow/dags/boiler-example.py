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

workspace_name = os.getenv("HD_WS_BOILERPLATE_NAME", "ws-boilerplate")
namespace = os.getenv("HD_NAMESPACE", "default")

# This will use .kube/config for local Astro CLI Airflow and ENV variable for k8s deployment
if namespace == "default":
    config_file = "include/.kube/config"  # copy your local kube file to the include folder: `cp ~/.kube/config include/.kube/config`
    in_cluster = False
else:
    in_cluster = True
    config_file = None

with DAG(
    dag_id="run_boiler_example",
    schedule="@once",
    default_args=default_args,
    description="Boiler Plate for running a hello data workspace in airflow",
    tags=[workspace_name],
) as dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="hellodata-ws-boilerplate:v1",
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred-azurecr")],
        labels={"pod-label-test": "label-name-test"},
        name="airflow-running-dagster-workspace",
        task_id="run_duckdb_query",
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
        # please add/overwrite your command here
        cmds=["/bin/bash", "-cx"],
        arguments=[
            "python query_duckdb.py && echo 'Query executed successfully'",  # add your command here
        ],
    )
