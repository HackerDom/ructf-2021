FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY xss_runner.py .
COPY user_agent_randomizer.py .
COPY useragents .

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:31337", "--workers", "1", "--worker-connections", "2048", "xss_runner:app" ]
