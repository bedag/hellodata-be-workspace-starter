
build:
	./build-and-push.sh 0.1.0 a.1

docker-test:
	docker run hellodata-ws-boilerplate:0.1.0-a.1

docker-it: # run dockerimage and ssh into contianer (interactive to test if things are working)
	docker run --rm -it --entrypoint /bin/bash hellodata-ws-boilerplate:0.1.0-a.1

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


create-volume-mount:
	kubectl apply -f src/volume-mount/pvc.yaml

get-volume-mount:
	kubectl get pvc
	kubectl get pv
