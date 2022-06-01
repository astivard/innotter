FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip
RUN pip install pipenv && pipenv lock && pipenv install --dev --system --deploy --ignore-pipfile

RUN adduser -u 5432 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]