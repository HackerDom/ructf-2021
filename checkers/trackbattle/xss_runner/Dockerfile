FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY app.py .
COPY user_agent_randomizer.py .
COPY useragents .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=31337" ]
# ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:31337", "--workers", "1", "--worker-connections", "2048", "xss_runner:app" ]
