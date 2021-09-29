#!/bin/bash
set -e -x

docker run --rm -iv $PWD:/app -w/app golang:latest  sh -s <<EOF
set -e -x
go mod vendor
go build .
EOF

stat container-service-gin
