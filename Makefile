poetry_install_dev:
	poetry install --with test --sync

poetry_install:
	poetry install --sync

build:
	docker compose build

up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

migrate_db:
	alembic upgrade head

dev:
	@echo "Starting MySQL container..."
	@docker compose up -d --build stock-microservice-db
	@echo "Waiting for MySQL to be ready..."
	@until docker compose exec stock-microservice-db mysqladmin ping -h localhost --silent; do \
		echo "Waiting for database connection..."; \
		sleep 2; \
	done
	@echo "MySQL is ready!"
	@sleep 2
	@echo "Applying migrations..."
	@MYSQL_HOST=localhost ./config/init_db/init_db.sh
	@echo "Starting Uvicorn..."
	@trap 'docker compose down --remove-orphans' INT TERM EXIT; \
	MYSQL_HOST=localhost uvicorn src.app:app --reload --host 0.0.0.0 --port 8003

test_watch:
	ENV=test ptw --runner 'pytest --ff $(extra)'

test_parallel:
	ENV=test pytest --cov=src --numprocesses auto --dist loadfile --max-worker-restart 0 $(extra)

test_last_failed:
	ENV=test ptw --runner 'pytest --ff --lf $(extra)'

test_coverage:
	coverage report --omit=tests/*
