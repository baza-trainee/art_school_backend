FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt ./
COPY scripts scripts/

RUN chmod a+x scripts/*.sh && \
    pip install -r requirements.txt

COPY src src/
COPY static static/
COPY migrations migrations/
COPY gunicorn.conf.py alembic.ini ./
