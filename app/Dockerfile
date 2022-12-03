FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY ./app/requirements.txt /app/

RUN pip install -r requirements.txt

COPY ./app /app