#!/bin/bash

set -e

submit_job()
{
	curl --location --request PUT 'http://'$1':8000/api/v1/jobs' \
	--header 'Content-Type: application/octet-stream' \
	--data-binary '@'$2
}

get_job_result()
{
	curl --location --request GET 'http://'$1':8000/api/v1/jobs/'$2
}
