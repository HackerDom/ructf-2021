#!/bin/bash
set -e -x

rm -rf $PWD/artifacts
mkdir $PWD/artifacts
docker build --tag allocmemory .
docker run --rm -iv $PWD:/app allocmemory  sh -s <<EOF
set -e -x
mkdir out
cp main.c CMakeLists.txt private.key out/
cd out
cmake --clean-first --configure .
cmake --build .
cp allocmemory ..
EOF