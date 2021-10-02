#!/bin/bash

KEY_DIR=/etc/container-svc/
KEY_NAME=secret.key
KEY_PATH=$KEY_DIR$KEY_NAME

# prepare the container image
docker build --tag=basealpine /root/container-svc/docker/

# generate the container users
for i in {1000..1200}; do adduser -u $i user$i --disabled-password; done

# create service key
if test -f "$KEY_PATH"; then
    echo "$KEY_PATH exists, skip creating..."
    exit 0
fi

mkdir -p $KEY_DIR
chmod 755 $KEY_DIR

echo "---BEGIN SERVICE PRIVATE KEY---" > $KEY_PATH
tr -dc A-Za-z0-9 </dev/urandom | head -c 320000 ; echo '' >> $KEY_PATH
echo "---END SERVICE PRIVATE KEY---" >> $KEY_PATH

chmod 755 $KEY_PATH
