#!/bin/bash

# Copy DAGs to local deployment directory
cp -r src/dags/*.py deployment/local/airflow/dags/

# Set Docker image tag and registry
DOCKER_IMAGE_TAG="local-build"
DOCKER_REGISTRY="my-docker-registry/path"

echo "DOCKER_IMAGE_TAG: ${DOCKER_IMAGE_TAG}"
IMAGE_NAME="${DOCKER_REGISTRY}/hellodata-ws-boilerplate:${DOCKER_IMAGE_TAG}"
echo "IMAGE_NAME: ${IMAGE_NAME}"

# Build Docker image
docker build -t "${IMAGE_NAME}" -f Dockerfile --build-arg DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG}" --platform "linux/amd64" .
