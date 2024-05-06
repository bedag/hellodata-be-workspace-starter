@echo off
if "%~1"=="" (
  echo.
  echo Usage:   .\build-and-push.cmd ^<RELEASE^> ^<DEV_STAGE^>
  echo.
  echo Example: .\build-and-push.cmd 0.1.0
  echo.
  exit /b 0
)

set proxy=%http_proxy%
if "%proxy%"=="" (
  set proxy=%HTTP_PROXY%
)
echo Using proxy: %proxy%

set noproxy=%no_proxy%
if "%noproxy%"=="" (
  set noproxy=%NO_PROXY%
)
if "%noproxy%"=="" (
  set noproxy=localhost
)
echo Using no_proxy: %noproxy%

set RELEASE=%~1
set DOCKER_IMAGE_TAG=%RELEASE%

set DOCKER_REGISTRY=my-docker-registry/path

echo DOCKER_IMAGE_TAG: %DOCKER_IMAGE_TAG%
set IMAGE_NAME=%DOCKER_REGISTRY%/hellodata-ws-boilerplate:%DOCKER_IMAGE_TAG%
echo IMAGE_NAME: %IMAGE_NAME%

docker build -t %IMAGE_NAME% -f Dockerfile --build-arg RELEASE=%RELEASE% --build-arg DEV_STAGE=%DEV_STAGE% --build-arg DOCKER_IMAGE_TAG=%DOCKER_IMAGE_TAG% --build-arg http_proxy=%proxy% --build-arg https_proxy=%proxy%  --build-arg no_proxy=%noproxy% --build-arg HTTP_PROXY=%proxy% --build-arg HTTPS_PROXY=%proxy%  --build-arg NO_PROXY=%noproxy% --platform "linux/amd64" .

:: uncomment when configured your docker hub as part of your docker image name
docker push %IMAGE_NAME%
