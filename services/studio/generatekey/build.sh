#!/bin/bash
set -e -x

docker build --tag generatekey .
docker run --rm -iv $PWD:/app generatekey  sh -s <<EOF
set -e -x
rm -rf out
mkdir out
cp main.c CMakeLists.txt private.key out/
cd out
cmake --clean-first --configure .
cmake --build .
cp generatekey ..
EOF