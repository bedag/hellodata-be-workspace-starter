
build:
	docker build -t hellodata-ws-boilerplate:local-build .

docker-test:
	docker run hellodata-ws-boilerplate:local-build

docker-it: # run dockerimage and ssh into contianer (interactive to test if things are working)
	docker run --rm -it --entrypoint /bin/bash hellodata-ws-boilerplate:local-build

create-volume-mount:
	kubectl apply -f deployment/volume-mount/pvc.yaml

get-volume-mount:
	kubectl get pvc
	kubectl get pv


astro-start:
	cd deployment/local/airflow/
	astro dev start -e ../env

astro-stop:
	cd deployment/local/airflow/
	astro dev stop

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
