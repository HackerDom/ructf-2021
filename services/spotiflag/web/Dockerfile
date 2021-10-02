FROM python:3.9-alpine

RUN adduser -s /bin/false -D -H -u 1000 spotiflag

RUN mkdir -p /var/spotiflag/

WORKDIR /var/spotiflag/

COPY service/requirements.txt ./

RUN pip install -r requirements.txt

COPY service .

USER spotiflag

ENTRYPOINT ["uvicorn", "--workers", "8", "--host", "0.0.0.0", "server:app"]
