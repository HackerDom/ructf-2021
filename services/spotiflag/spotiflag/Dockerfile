FROM ubuntu:20.04

RUN apt update \
    && apt install -y libquadmath0

RUN useradd --no-create-home --shell /bin/false --uid 1000 --user-group spotiflag

RUN mkdir /tmp/songs/ /tmp/spotiflag/ \
    && chown spotiflag:spotiflag /tmp/songs/ /tmp/spotiflag/

COPY spotiflag /

RUN chmod +x /spotiflag

USER spotiflag

ENTRYPOINT ["/spotiflag"]
