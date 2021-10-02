#!/bin/bash

set -ex

packer build --force build.pkr.hcl

# Due to https://www.virtualbox.org/ticket/19440
rm output-studio/*.mf
