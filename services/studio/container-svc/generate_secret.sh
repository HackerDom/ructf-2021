#!/bin/bash

KEY_PATH=/root/container-svc/secret.key

if test -f "$KEY_PATH"; then
    echo "$KEY_PATH exists, skip creating..."
    exit 0
fi

echo "---BEGIN SERVICE PRIVATE KEY---" > $KEY_PATH
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 320000 | head -n 1 >> $KEY_PATH
echo "---END SERVICE PRIVATE KEY---" >> $KEY_PATH
