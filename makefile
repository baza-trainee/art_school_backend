.PHONY: down build run

down:
	docker compose down

run: down 
	docker compose up postgres -d
	sleep 2
	alembic upgrade head
	uvicorn vercel:app --reload

start:
	uvicorn vercel:app --reload

build: down
	docker compose up -d

open-redis:
	docker exec -it fastapi-redis redis-cli
