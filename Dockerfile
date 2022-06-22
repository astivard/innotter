FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv lock && pipenv install --system

COPY . /app/

RUN chmod +x ./entrypoint.sh
RUN chmod +x ./entrypoint_celery.sh
