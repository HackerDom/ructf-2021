FROM python:3.8-slim

WORKDIR /app

COPY ./src/back/ .

RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:31337", "--workers", "4", "--worker-connections", "2048", "app:app" ]

