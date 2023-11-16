.PHONY: init init-migration down build run db-migrate test tox

down:
	docker compose down

run: build upgrade
	uvicorn src.main:app --reload

build:
	docker compose up -d

migrate:
	alembic revision --autogenerate -m

upgrade:
	alembic upgrade head
