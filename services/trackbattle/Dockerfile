FROM python:3.8-slim

WORKDIR /app

COPY ./src/back/requirements.txt ./
RUN pip install -r requirements.txt

COPY src/back/ .

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:31337", "--workers", "1", "--worker-connections", "2048", "app:app" ]

