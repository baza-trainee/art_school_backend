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
	docker compose up -d --build

open-redis:
	docker exec -it fastapi-redis redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

backup:
	chmod +x scripts/backup.sh
	if crontab -l 2>/dev/null; then crontab -l > mycron; else touch mycron; fi
	echo "*/1 * * * * $(PWD)/scripts/backup.sh" >> mycron
	crontab mycron
	rm mycron

restore:
	chmod +x scripts/restore.sh
	./scripts/restore.sh
