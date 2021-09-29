#!/bin/bash

KEY_PATH=/root/container-svc/secret.key

if test -f "$KEY_PATH"; then
    echo "$KEY_PATH exists, skip creating..."
    exit 0
fi

echo "---BEGIN SERVICE PRIVATE KEY---" > $KEY_PATH
tr -dc A-Za-z0-9 </dev/urandom | head -c 320000 ; echo '' >> $KEY_PATH
echo "---END SERVICE PRIVATE KEY---" >> $KEY_PATH
