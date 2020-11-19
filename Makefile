.PHONY: build, test, help
.DEFAULT_GOAL := help
SHELL:=/bin/bash

IMAGE_NAME=dkr-ls
LATEST=$(IMAGE_NAME):latest

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build: Dockerfile ## Build the Dcokerfile and tag it as latest
	docker build . -t $(IMAGE_NAME)
	docker tag $(IMAGE_NAME) $(LATEST)

test: ## run Python unit tests - assumes that dependencies have been installed
	python -m pytest -vv
