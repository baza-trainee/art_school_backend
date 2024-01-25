FROM python:3.11-slim

RUN mkdir /backend_app

WORKDIR /backend_app

COPY requirements.txt ./
COPY scripts scripts/

RUN chmod a+x scripts/*.sh
RUN pip install -r requirements.txt

COPY src src/
COPY static static/
COPY migrations migrations/
COPY gunicorn.conf.py alembic.ini ./
