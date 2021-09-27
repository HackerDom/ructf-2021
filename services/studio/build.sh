#!/bin/bash

set -e

PATH=$PATH:/usr/local/go/bin make build -C container-svc -j4