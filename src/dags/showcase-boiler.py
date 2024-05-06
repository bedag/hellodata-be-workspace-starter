from pendulum import datetime
from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s

import os
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
DATA_PATH = os.getenv("DATA_PATH")
WORKSPACE_NAME = os.getenv("HD_WS_BOILERPLATE_NAME")
NAMESPACE = os.getenv("HD_NAMESPACE")
VOLUME_CLAIM_NAME = os.getenv("VOLUME_CLAIM_NAME")
VOLUME_NAME = os.getenv("VOLUME_NAME")


# This will use .kube/config for local Astro CLI Airflow and ENV variable for k8s deployment
if NAMESPACE == "default":
    config_file = "include/.kube/config"  # copy your local kube file to the include folder: `cp ~/.kube/config include/.kube/config`
    in_cluster = False
else:
    in_cluster = True
    config_file = None


volume_claim = k8s.V1PersistentVolumeClaimVolumeSource(claim_name=VOLUME_CLAIM_NAME)
volume = k8s.V1Volume(name=VOLUME_NAME, persistent_volume_claim=volume_claim)
volume_mount = k8s.V1VolumeMount(name=VOLUME_NAME, mount_path=DATA_PATH)

# Define common parameters for KubernetesPodOperator tasks
common_k8s_pod_operator_params = {
    "namespace": NAMESPACE,
    "image": "hellodata-ws-boilerplate:local-build",
    "image_pull_secrets": [k8s.V1LocalObjectReference("regcred-azurecr")],
    "get_logs": True,
    "is_delete_operator_pod": True,
    "labels": {"pod-label-test": "label-name-test"},
    "in_cluster": in_cluster,
    "cluster_context": "docker-desktop",
    "config_file": config_file,
    "cmds": ["/bin/bash", "-cx"],
    "volumes": [volume],
    "volume_mounts": [volume_mount],
    "env_vars": {
        # Add all env variables you need from deployment/env file
        "HD_WS_BOILERPLATE_NAME": os.getenv("HD_WS_BOILERPLATE_NAME"),
        "HD_NAMESPACE": os.getenv("HD_NAMESPACE"),
        "POSTGRES_USERNAME": os.getenv("POSTGRES_USERNAME"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_DATABASE": os.getenv("POSTGRES_DATABASE"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "SQL_SCHEMA_NAME": os.getenv("SQL_SCHEMA_NAME"),
        "VOLUME_CLAIM_NAME": os.getenv("VOLUME_CLAIM_NAME"),
        "VOLUME_NAME": os.getenv("VOLUME_NAME"),
        "DATA_PATH": os.getenv("DATA_PATH"),
    },
}

with DAG(
    dag_id="run_showcase_boiler_example",
    schedule="@once",
    default_args=default_args,
    description="Showcase to run Airflow and dbt on hello data workspace in airflow",
    tags=[WORKSPACE_NAME],
) as dag:
    data_download = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="data-download",
        task_id="data_download",
        arguments=[
            "python showcase.py --data_download && echo 'download successfully'"
        ],
    )

    create_tables = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="create-tables",
        task_id="create_tables",
        arguments=[
            "python showcase.py --create_tables && echo 'created tables successfully'"
        ],
    )

    insert_data = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="insert-data",
        task_id="insert_data",
        arguments=[
            "python showcase.py --insert_data && echo 'insert data successfully'"
        ],
    )

    dbt_run = KubernetesPodOperator(
        **common_k8s_pod_operator_params,
        name="dbt-run",
        task_id="dbt_run",
        arguments=[
            "cd /usr/src/dbt/ && dbt deps && dbt run && echo 'dbt run successfully' && dbt docs generate --target-path /usr/src/dbt-docs && echo 'dbt docs generate successfully'",
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
