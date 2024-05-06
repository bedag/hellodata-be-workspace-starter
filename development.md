
# Development


## Starting local postgres with predefined schema

This will create the database `svsa` and its relevant table for developing locally with schema `a02a`.
```sh
cd src/postgres-setup-local/
docker-compose up -d
```

to stop just run `docker-compose down` or `docker-compose down --volumes --remove-orphans` to remove the volume as well.


## Run Airflow locally 

- activate kubernetes in docker desktop
- Copy the kube config to the airflow deployment folder
- Create volumne (initially): `kubectl apply -f deployment/volume-mount/pvc.yaml`
- pip install `apache-airflow-providers-cncf-kubernetes` in case you get a missing requirements (should be installed by astro automatically)
- Check that context of kubernetes is set to docker-desktop `kubectl config current-context` (set with `kubectl config use-context docker-desktop`)

```sh
#linux
cp ~/.kube/config deployment/local/airflow/include/.kube/

#windows
xcopy %USERPROFILE%\.kube\config deployment\local\airflow'include\.kube\
```


and start Astro (install astro first)

```sh
cd deployment/local/airflow
astro dev start -e ../env
```

### Running Docker image locally (development)

Opposed to running the dag within Astro (which would be the normal use-case as shown above), you can run and test the docker image locally as well. This allows a little faster developer cycles (you save the running airflow and the full dag and you can test/develop dedicated steps).

This way you need to manually set (export) the environment variables as these are not set through Airflow (who starts and sets these automatically). 

This is how you'd run the image you created and go inside the container:

```sh
docker run -it hellodata-ws-boilerplate:local-build bash
```

This is how you set the environment variables and:
```sh
export POSTGRES_USERNAME_HD=postgres
export POSTGRES_PASSWORD_HD=postgres
export POSTGRES_HOST_HD=host.docker.internal
export POSTGRES_DATABASE_HD=svsa
export POSTGRES_PORT_HD="5444"
```

Run and test dbt:

```sh
cd dbt
dbt compile
dbt run
```

