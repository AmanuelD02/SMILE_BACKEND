ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build -d --remove-orphans
up:
	docker-compose up -d
down:
	docker-compose down
logs:
	docker-compose logs

migragte:
	docker-compose exec app python manage.py migrate --noinput

makemigrations:
	docker-compose exec app python manage.py makemigrations


superuser:
	docker-compose exec app manage.py createsuperuser

volume:
	docker volume inspect smile_backend-src_postgres_data 

shell:
	docker-compose exec app python manage.py shell