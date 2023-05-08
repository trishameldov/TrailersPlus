.DEFAULT_GOAL := help
WEB_CONTAINER=web
CELERY_CONTAINER=celery
DATABASE_CONTAINER=db
DOCKER_COMPOSE_FILE= ./docker/docker-compose.yml

build:
	docker-compose -f $(DOCKER_COMPOSE_FILE)  up --build --remove-orphans -d

server:
	docker exec -it $(WEB_CONTAINER) python manage.py runserver 0.0.0.0:8000

migrate:
	docker exec -it $(WEB_CONTAINER) python manage.py migrate

migrations:
	docker exec -it $(WEB_CONTAINER) python manage.py makemigrations --noinput

createsuperuser:
	docker exec -it $(WEB_CONTAINER) python manage.py createsuperuser

collectstatic:
	docker exec -it $(WEB_CONTAINER) python manage.py collectstatic --noinput

shell:
	docker exec -it $(WEB_CONTAINER) python manage.py shell

test:
	docker exec -it $(WEB_CONTAINER) python manage.py test

flake8:
	docker exec -it $(WEB_CONTAINER) flake8

up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

stop:
	docker-compose -f $(DOCKER_COMPOSE_FILE) stop

ssh:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec $(WEB_CONTAINER) /bin/bash

ssh-db:
	docker exec -it $(DATABASE_CONTAINER) /bin/bash

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

restart:
	docker-compose -f $(DOCKER_COMPOSE_FILE) restart

logs:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f $(WEB_CONTAINER)

logs-celery:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f $(CELERY_CONTAINER)

logs-db:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f $(DATABASE_CONTAINER)

help:
	@echo 'Management commands for trailersplus:'
	@echo
	@echo 'Usage:'
	@echo '    make build              Build docker containers'
	@echo '    make up                 Start docker containers'
	@echo '    make server             Run development server'
	@echo '    make stop               Stop docker containers'
	@echo '    make down               Stop and remove docker containers, networks, images, and volumes'
	@echo '    make restart            Restart docker containers'
	@echo '    make ssh                SSH into web container'
	@echo '    make ssh-db             SSH into db container'
	@echo '    make migrate            Run migrations'
	@echo '    make migrations         Create migrations'
	@echo '    make createsuperuser    Create superuser'
	@echo '    make collectstatic      Collect static files'
	@echo '    make shell              Run django shell'
	@echo '    make test               Run django tests'
	@echo '    make flake8             Run flake8'
	@echo '    make logs               View web container logs'
	@echo '    make logs-celery        View celery container logs'
	@echo '    make logs-db            View db container logs'
	@echo '    make help               Show this help message'
