IMAGE_NAME=dkr-ls
LATEST=$(IMAGE_NAME):latest

build: Dockerfile
	docker build . -t $(IMAGE_NAME)
	docker tag $(IMAGE_NAME) $(LATEST)

# run Python unit tests
# this assumes that dependencies have been installed
test:
	python -m pytest -vv

.PHONY: build, test
.DEFAULT_GOAL := test
