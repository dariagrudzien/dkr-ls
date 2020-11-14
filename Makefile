IMAGE_NAME=dkr-ls
LATEST=$(IMAGE_NAME):latest

build: Dockerfile
	docker build . -t $(IMAGE_NAME)
	docker tag $(IMAGE_NAME) $(LATEST)

.PHONY: build
.DEFAULT_GOAL := build
