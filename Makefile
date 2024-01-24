.PHONY: down build run prod drop_db backup restore prune frontend_build frontend_export

BACKUP_COMMAND := * * * * * cd "$(PWD)" && python3 scripts/backup.py

prod:
	@if [ $$(docker ps -q -f name=backend) ]; then \
			docker compose stop backend; \
			docker compose rm -f backend; \
	fi
	docker compose up -d --build

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
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo '$(BACKUP_COMMAND)' >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"

stop_backup:
	crontab -l | grep -v '$(BACKUP_COMMAND)' | crontab -

restore:
	python3 scripts/restore.py

frontend_build:
	tar -cJvf dist.tar.xz dist

frontend_export:
	tar -xJvf dist.tar.xz -C .

drop_db: down
	docker volume rm $$(basename "$$(pwd)")_postgres_data
	docker volume rm $$(basename "$$(pwd)")_redis_data

prune: down
	docker system prune -a
	docker volume prune -a