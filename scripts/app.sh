sleep 10
alembic upgrade head
gunicorn -c gunicorn.conf.py src.main:app
