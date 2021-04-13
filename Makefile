PORT := 8080
REGION := fr-par
REGISTRY_ENDPOINT := rg.$(REGION).scw.cloud
REGISTRY_NAMESPACE := matomo
NAME := matomo
IMAGE_NAME := $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE)/$(NAME)
VERSION := latest
TAG := $(IMAGE_NAME):$(VERSION)

BASE_URL := 'https://stats.data.gouv.fr/'
build:
	docker build -t $(TAG) .

start:
	docker run -e PORT=$(PORT) -p $(PORT):$(PORT) ${IMAGE_NAME}

login:
	docker login $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE) -u nologin -p $(SCW_SECRET_TOKEN)

push:
	docker push $(IMAGE_NAME)

deploy:
	@make build
	@make login
	@make push

run: 
	@make build
	@make start

