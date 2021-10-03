#!/bin/bash
set -e -x

docker build --tag checker_payload .
docker run --rm -iv $PWD:/app checker_payload  sh -s <<EOF
set -e -x
rm -rf out
mkdir out
cp main.c CMakeLists.txt out/
cd out
cmake --clean-first --configure .
cmake --build .
cp checker_payload ..
EOF