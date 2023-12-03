.PHONY: down build run

down:
	docker compose down

run: down
	docker compose up postgres -d
	alembic upgrade head
	sleep 2
	uvicorn vercel:app --reload

start:
	uvicorn vercel:app --reload

build: down
	docker compose up -d

open-redis:
	docker exec -it fastapi-redis redis-cli
