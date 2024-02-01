#!/bin/bash
if  [ -z "$1" ] || [ -z "$2" ]; then
  echo ""
  echo "Usage:   .\build-and-push.sh <RELEASE> <DEV_STAGE>"
  echo ""
  echo "Example: .\build-and-push.sh 0.1.0 a.1"
  echo ""
  exit 0
fi

proxy=$http_proxy
if [ -z "$proxy" ]; then
  proxy=$HTTP_PROXY
fi
echo "Using proxy: " $proxy

noproxy=$no_proxy
if [ -z "$noproxy" ]; then
  noproxy=$NO_PROXY
fi
if [ -z "$noproxy" ]; then
  noproxy=localhost
fi
echo "Using no_proxy: " $noproxy

RELEASE=$1
DEV_STAGE=$2
DOCKER_IMAGE_TAG=$RELEASE-$DEV_STAGE

echo "DOCKER_IMAGE_TAG: "${DOCKER_IMAGE_TAG}
IMAGE_NAME=hellodata-ws-boilerplate:$DOCKER_IMAGE_TAG
echo "IMAGE_NAME: "${IMAGE_NAME}
docker build -t $IMAGE_NAME -f Dockerfile --build-arg RELEASE=$RELEASE --build-arg DEV_STAGE=$DEV --build-arg DOCKER_IMAGE_TAG=$DOCKER_IMAGE_TAG --build-arg http_proxy=$proxy --build-arg https_proxy=$proxy  --build-arg no_proxy=$noproxy --build-arg HTTP_PROXY=$proxy --build-arg HTTPS_PROXY=$proxy  --build-arg NO_PROXY=$noproxy --platform "linux/amd64" .
#comment in when configured your docker hub as part of your docker image name
#docker push $IMAGE_NAME
