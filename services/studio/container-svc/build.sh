#!/bin/bash
set -e -x

go build -v .

stat container-service-gin
