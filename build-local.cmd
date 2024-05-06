@echo off

xcopy "src\dags\*" "deployment\local\airflow\dags" /s /e /y

set DOCKER_IMAGE_TAG=local-build

set DOCKER_REGISTRY=my-docker-registry/path

echo DOCKER_IMAGE_TAG: %DOCKER_IMAGE_TAG%
set IMAGE_NAME=%DOCKER_REGISTRY%/hellodata-ws-boilerplate:%DOCKER_IMAGE_TAG%
echo IMAGE_NAME: %IMAGE_NAME%

docker build -t %IMAGE_NAME% -f Dockerfile --build-arg DOCKER_IMAGE_TAG=%DOCKER_IMAGE_TAG% --platform "linux/amd64" .
