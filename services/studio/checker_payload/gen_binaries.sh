#!/bin/bash

set -e
DST_FOLDER=generated
mkdir -p $DST_FOLDER

for i in `seq 1 $1`
do
  bash ./build.sh
  OFFSET=$(grep -oba PLACEHOLDERREPLACEMEWITHREALFLAG checker_payload | awk -F ':' '{print $1}')
  mv checker_payload $DST_FOLDER/$i"_"$OFFSET 
done

