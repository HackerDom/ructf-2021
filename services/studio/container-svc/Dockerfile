FROM golang:latest

WORKDIR $GOPATH/src/github.com/usernamedt/container-svc-gin
COPY . $GOPATH/src/github.com/usernamedt/container-svc-gin
RUN go build .

EXPOSE 8000
ENTRYPOINT ["./container-svc-gin"]
