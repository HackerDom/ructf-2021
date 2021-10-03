#!/bin/bash
set -e -x

docker build --tag vuln .
docker run --rm -iv $PWD:/app vuln  sh -s <<EOF
set -e -x
rm -rf out
mkdir out
cp main.c CMakeLists.txt out/
cd out
cmake --clean-first --configure .
cmake --build .
cp vuln ..
EOF