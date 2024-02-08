# Workspace `Boiler Plate`

This is a the boiler-plate workspace that you can clone and add your requirements. This should help you to understand how to set up a project within HelloDATA.

Goal: that you can test and create your DAGs, dbt, and whatever you need within this git-repo and deploy anywhere with regular HelloDATA deployment.

We use a [Airflow DAGs](/src/dags/airflow/dags) that will be copied with an initContainer into central Airflow orchestrator within Business Domain.

Find the detailed documentation on [Workspaces Documentation](https://kanton-bern.github.io/hellodata-be/concepts/workspaces/).

## Deployment

- the dags you are running on HelloDATA are in [/src/dags/airflow/dags/](/src/dags/airflow/dags/) folder. Check [boiler-example.py](/src/dags/airflow/dags/boiler-example.py) for an example
- add your deployments needs and requirements into [deployment needs](deployment/deployment-needs.yaml). This step will be integrated in your working HelloDATA environments.
  - make sure to set the ENV variable (e.g. postgres local password) on `deployment/dev`
- you can specify all your requirements in [Dockerfile](Dockerfile)
- build your image with `docker build -t hellodata-ws-boilerplate:v1 .` or create your own one. Be sure that your HelloDATA instance has access to your uploaded Docker registry.
  - see all comands in `Makefile`. If you want to check the docker file, run it interactively with `docker run -it hellodata-ws-boilerplate:v1 bash`

## Airflow locally (testing)

For testing your Airflow locally. You can use above menitoned Astro CLI, which makes it very easy to run Airflow with one command `	astro dev start -e ../../../deployment/env`. See more details on [Airflow Readme](/src/dags/airflow/README.md).

Requirements:
- Local Docker installed (either native or Docker-Desktop)
  - **Windows**: Enable in Docker Desktop under `Settings -> General -> Use WSL 2 based engine` the settings: `Add the *.docker.internal names to the host's etc/hosts file (Requires password)`
    - Make sure Docker-Desktop entered it correctly in `C:\Windows\System32\drivers\etc\hosts`. There were some [cases](https://github.com/kanton-bern/hellodata-be/issues/21#issuecomment-1913578206) where it added wrongly. It should look something like:
```sh
# Added by Docker Desktop
<YOUR-IP-HERE> host.docker.internal
<YOUR-IP-HERE> gateway.docker.internal
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section
```
  - make sure Kubernetes is enabled
- copy you local kube-file to astro: `cp ~/.kube/config src/dags/airflow/include/.kube/`
  - **Windows**: The file is under `%USERPROFILE%\.kube\config` (C:\Users\[YourIdHere]\.kube)
- install `KubernetesPodOperator` locally with pip (not with astro) install `pip install apache-airflow-providers-cncf-kubernetes`.
- if you store data from one task to the next, you need a volume-mount (see `pvc.yaml`) and configure `volumes` and `volume_mounts` in Airflow (see example)

