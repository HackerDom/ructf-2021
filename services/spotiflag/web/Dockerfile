FROM python:3.8-slim

RUN useradd --no-create-home --shell /bin/false --uid 1000 --user-group spotiflag

RUN mkdir -p /var/spotiflag/

WORKDIR /var/spotiflag/

COPY service/requirements.txt ./

RUN pip install -r requirements.txt

COPY service .

USER spotiflag

ENTRYPOINT ["uvicorn", "--workers", "8", "--host", "0.0.0.0", "server:app"]
