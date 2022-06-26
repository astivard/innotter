FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install fastapi==0.78.0 pydantic==1.9.1 uvicorn==0.18.1

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
