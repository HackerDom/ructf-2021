#!/bin/bash
set -e -x

docker build --tag deallocmemory .
docker run --rm -iv $PWD:/app deallocmemory  sh -s <<EOF
set -e -x
rm -rf out
mkdir out
cp main.c CMakeLists.txt out/
cd out
cmake --clean-first --configure .
cmake --build .
cp deallocmemory ..
EOF