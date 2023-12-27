FROM python:3.11-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt ./
COPY scripts scripts/

RUN chmod a+x scripts/*.sh && \
    pip install -r requirements.txt gunicorn==21.2.0 fastapi-cache2==0.2.0 redis==4.4.2

COPY src src/
COPY static static/
COPY migrations migrations/
COPY gunicorn.conf.py alembic.ini ./

EXPOSE 8000
