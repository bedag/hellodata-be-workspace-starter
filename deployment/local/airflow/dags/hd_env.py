from kubernetes.client import models as k8s
import os

data_path = os.getenv("DATA_PATH")
workspace_name = "HD_WS_BOILERPLATE_NAME"
namespace = "default"
volume_claim_name = "my-pvc"
volume_name = "storage"

# This will use .kube/config for local Astro CLI Airflow and ENV variable for k8s deployment
config_file = "include/.kube/config"  # copy your local kube file to the include folder: `cp ~/.kube/config include/.kube/config`
in_cluster = False

volume_claim = k8s.V1PersistentVolumeClaimVolumeSource(claim_name=volume_claim_name)
volume = k8s.V1Volume(name=volume_name, persistent_volume_claim=volume_claim)
volume_mount = k8s.V1VolumeMount(name=volume_name, mount_path=data_path)

# Define common parameters for KubernetesPodOperator tasks
common_k8s_pod_operator_params = {
    "namespace": namespace,
    "image": "my-docker-registry/path/hellodata-ws-boilerplate:local-build",
    #"image_pull_secrets": [k8s.V1LocalObjectReference("regcred-azurecr")],
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
        # Add all env variables you need from deployment/local/env file
        "DATA_PATH": os.getenv("DATA_PATH"),

        "POSTGRES_USERNAME_HD": os.getenv("POSTGRES_USERNAME_HD"),
        "POSTGRES_PASSWORD_HD": os.getenv("POSTGRES_PASSWORD_HD"),
        "POSTGRES_HOST_HD": os.getenv("POSTGRES_HOST_HD"),
        "POSTGRES_DATABASE_HD": os.getenv("POSTGRES_DATABASE_HD"),
        "POSTGRES_PORT_HD": os.getenv("POSTGRES_PORT_HD"),
        "SQL_SCHEMA_NAME": os.getenv("SQL_SCHEMA_NAME"),

    },
}

