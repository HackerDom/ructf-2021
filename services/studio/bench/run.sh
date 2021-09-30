#!/bin/bash

set -e
source util.sh

SVC_HOST=localhost
PAYLOAD_PATH=/home/usernamedt/ctf/ructf-2021/services/studio/payload/payload


max="$1"
date
echo "rate: $max calls / second"
START=$(date +%s);

while true
do
  echo -e $(($(date +%s) - START)) | awk '{print int($1/60)":"int($1%60)}'
  echo -e $(date)
  sleep 1

  for i in `seq 1 $max`
  do
	 submit_job $SVC_HOST $PAYLOAD_PATH &
  done
done

