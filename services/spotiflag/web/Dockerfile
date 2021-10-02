FROM python:3.8-slim

RUN adduser -s /bin/false -D -H -u 1000 spotiflag

RUN mkdir -p /var/spotiflag/

WORKDIR /var/spotiflag/

COPY service/requirements.txt ./

RUN pip install -r requirements.txt

COPY service .

ENTRYPOINT ["uvicorn", "--workers", "8", "--host", "0.0.0.0", "server:app"]
