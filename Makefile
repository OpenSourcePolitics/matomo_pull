PORT := 8080
REGION := fr-par
REGISTRY_ENDPOINT := rg.$(REGION).scw.cloud
REGISTRY_NAMESPACE := funcscwmtmtestxx0tvv6o
NAME := matomo
IMAGE_NAME := $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE)/$(NAME)
VERSION := latest
TAG := $(IMAGE_NAME):$(VERSION)

build:
	docker build -t $(TAG) . --compress

start:
	docker run -e JWT_SECRET_KEY=$(JWT_SECRET_KEY)\
		-e POSTGRES_USER=$(POSTGRES_USER)\
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)\
		-e POSTGRES_HOST=$(POSTGRES_HOST)\
		-e POSTGRES_PORT=$(POSTGRES_PORT)\
		-p $(PORT):$(PORT)\
		${IMAGE_NAME}

stop:
	docker ps --filter 'ancestor=$(IMAGE_NAME)' --format '{{.Names}}' | xargs docker stop

login:
	docker login $(REGISTRY_ENDPOINT)/$(REGISTRY_NAMESPACE) -u nologin -p $(SCW_SECRET_TOKEN)

push:
	docker push $(IMAGE_NAME)

deploy:
	@make login
	@make build
	@make push

run: 
	@make build
	@make start

restart:
	@make stop
	@make run

test:
	curl localhost:$(PORT)