.PHONY: init init-migration down build run db-migrate test tox

down:
	docker compose down

run: build upgrade
	uvicorn vercel:app --reload

start:
	uvicorn vercel:app --reload

build:
	docker compose up -d
	sleep 2

migrate:
	alembic revision --autogenerate -m

upgrade:
	alembic upgrade head
