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

auto_backup:
	@if crontab -l ; then \
		crontab -l > mycron ; \
	else \
		touch mycron ; \
	fi
	@echo '$(BACKUP_COMMAND)' >> mycron
	@crontab mycron
	@rm mycron
	@echo "Backup script added to cron"

backup:
	python3 scripts/backup.py
	@echo "Backup complete"
	
stop_backup:
	crontab -l | grep -v '$(BACKUP_COMMAND)' | crontab -

restore:
	python3 scripts/restore.py

frontend_build:
	tar -cJvf dist.tar.xz dist

frontend_export:
	if [ -d /var/www/school/dist ]; then \
		sudo rm -rf /var/www/school/dist; \
	fi
	sudo mkdir -p /var/www/school/
	sudo tar -xJvf dist.tar.xz -C /var/www/school/


drop_db: down
	if docker volume ls -q | grep -q $$(basename "$$(pwd)")_postgres_data; then \
		docker volume rm $$(basename "$$(pwd)")_postgres_data; \
		echo "successfully drop_db command";\
	fi
	sudo rm -rf ./static/media

prune: down
	docker system prune -a
	docker volume prune -a