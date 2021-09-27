#!/bin/bash

GO_VER=1.17.1

curl -O https://dl.google.com/go/go$GO_VER.linux-amd64.tar.gz
sudo tar -xvf go1.12.1.linux-amd64.tar.gz -C /usr/local
sudo chown -R root:root /usr/local/go