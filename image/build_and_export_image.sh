#!/bin/bash

set -ex

wget -N http://releases.ubuntu.com/20.04/ubuntu-20.04.3-server-amd64.iso

packer build --force build.pkr.hcl

# Due to https://www.virtualbox.org/ticket/19440
rm output-sandbox/*.mf
