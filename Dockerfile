FROM python:3.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt gunicorn==21.2.0 fastapi-cache2==0.2.0 redis==4.4.2

COPY . .
