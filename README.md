# Workspace `Boiler Plate`

This is a the boiler-plate workspace that you can clone and add your requirements. This should help you to understand how to set up a project within HelloDATA.

Goal: that you can test and create your DAGs, dbt, and whatever you need within this git-repo and deploy anywhere with regular HelloDATA deployment.

We use a [Airflow DAGs](/src/dags/airflow/dags) that will be copied with an initContainer into central Airflow orchestrator within Business Domain.

Find the detailed documentation on [Workspaces Documentation](https://kanton-bern.github.io/hellodata-be/concepts/workspaces/).

## Deployment

- the dags you are running on HelloDATA are in [/src/dags/airflow/dags/](/src/dags/airflow/dags/) folder. Check [boiler-example.py](/src/dags/airflow/dags/boiler-example.py) for an example
- add your deployments needs and requirements into [deployment needs](deployment/deployment-needs.yaml). This step will be integrated in your working HelloDATA environments.
- you can specify all your requirements in [Dockerfile](Dockerfile)
- build your image with [build-and-push.sh](build-and-push.sh) or create your own one. Be sure that your HelloDATA instance has access to your uploaded Docker registry.


## Airflow locally (testing)

For testing your Airflow locally. You can use above menitoned Astro CLI, which makes it very easy to run Airflow with one command `astro start`. See more details on [Airflow Readme](/src/dags/airflow/README.md).

Requirements:
- Local Docker installed (either native or Docker-Desktop)
- make sure Kubernetes is enables
- copy you local kube-file to astro: `mkdir src/dags/airflow/include/ && mkdir && src/dags/airflow/include/.kube/ && cp ~/.kube/config src/dags/airflow/include/.kube/`
- install `KubernetesPodOperator` locally with pip (not with astro) install `pip install apache-airflow-providers-cncf-kubernetes`.
- if you store data from one task to the next, you need a volume-mount (see `pvc.yaml`) and configure `volumes` and `volume_mounts` in Airflow (see example)

