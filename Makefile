.PHONY: up bootstrap lint test test-backend test-intel test-frontend compose-prod docker-build docker-rebuild

up:
	docker compose up -d --build

docker-build:
	docker compose build api frontend intelligence_api

docker-rebuild:
	docker compose build --no-cache api frontend intelligence_api

bootstrap:
	./scripts/bootstrap-champeng.sh

lint:
	cd sentinelx-backend && ruff check app tests
	cd sentinelx-intelligence && ruff check app tests
	cd sentinelx-frontend && npm run lint

test: test-backend test-intel test-frontend

test-backend:
	cd sentinelx-backend && pytest -q

test-intel:
	cd sentinelx-intelligence && pytest -q

test-frontend:
	cd sentinelx-frontend && npm run test

compose-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml config --quiet
