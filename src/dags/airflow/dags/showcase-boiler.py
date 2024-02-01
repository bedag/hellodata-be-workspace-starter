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

workspace_name = os.getenv("HD_WS_BOILERPLATE_NAME", "ws-boilerplate")
namespace = os.getenv("HD_NAMESPACE", "default")

# This will use .kube/config for local Astro CLI Airflow and ENV variable for k8s deployment
if namespace == "default":
    config_file = "include/.kube/config"  # copy your local kube file to the include folder: `cp ~/.kube/config include/.kube/config`
    in_cluster = False
else:
    in_cluster = True
    config_file = None


volume_claim = k8s.V1PersistentVolumeClaimVolumeSource(claim_name="my-pvc")
volume = k8s.V1Volume(name="my-volume", persistent_volume_claim=volume_claim)
volume_mount = k8s.V1VolumeMount(name="my-volume", mount_path="/mnt/pvc")


with DAG(
    dag_id="run_showcase_boiler_example",
    schedule="@once",
    default_args=default_args,
    description="Showcase to run Airflow and dbt on hello data workspace in airflow",
    tags=[workspace_name],
) as dag:
    data_download = KubernetesPodOperator(
        namespace=namespace,
        image="hellodata-ws-boilerplate:0.1.0-a.1",
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred-azurecr")],
        name="data-download",
        task_id="data_download",
        get_logs=True,
        is_delete_operator_pod=True,
        labels={"pod-label-test": "label-name-test"},
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        # please add/overwrite your command here
        cmds=["/bin/bash", "-cx"],
        arguments=[
            "python showcase.py --data_download && echo 'download successfully'",  # add your command here
        ],
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    create_tables = KubernetesPodOperator(
        namespace=namespace,
        image="hellodata-ws-boilerplate:0.1.0-a.1",
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred-azurecr")],
        name="create-tables",
        task_id="create_tables",
        get_logs=True,
        is_delete_operator_pod=True,
        labels={"pod-label-test": "label-name-test"},
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        # please add/overwrite your command here
        cmds=["/bin/bash", "-cx"],
        arguments=[
            "python showcase.py --create_tables && echo 'created tables successfully'",  # add your command here
        ],
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    insert_data = KubernetesPodOperator(
        namespace=namespace,
        image="hellodata-ws-boilerplate:0.1.0-a.1",
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred-azurecr")],
        name="insert-data",
        task_id="insert_data",
        get_logs=True,
        is_delete_operator_pod=True,
        labels={"pod-label-test": "label-name-test"},
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        # please add/overwrite your command here
        cmds=["/bin/bash", "-cx"],
        arguments=[
            "python showcase.py --insert_data && echo 'insert data successfully'",  # add your command here
        ],
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    dbt_run = KubernetesPodOperator(
        namespace=namespace,
        image="hellodata-ws-boilerplate:0.1.0-a.1",
        image_pull_secrets=[k8s.V1LocalObjectReference("regcred-azurecr")],
        name="dbt-run",
        task_id="dbt_run",
        get_logs=True,
        is_delete_operator_pod=True,
        labels={"pod-label-test": "label-name-test"},
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        # please add/overwrite your command here
        cmds=["/bin/bash", "-cx"],
        arguments=[
            "cd /usr/src/dbt/ && dbt deps && dbt run && echo 'dbt run successfully' && dbt docs generate --target-path /usr/src/dbt-docs && echo 'dbt docs generate successfully'",
        ],
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

    # Defining task dependencies
    (
        data_download
        >> create_tables
        >> insert_data
        >> dbt_run
        # >> dbt_docs_serve
    )
