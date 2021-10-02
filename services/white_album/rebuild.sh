#!/bin/bash

docker-compose -f docker-compose-build.yml down
docker-compose down

docker system prune --all -f

docker-compose -f docker-compose-build.yml up --build --remove-orphans --force-recreate
docker-compose up --build --force-recreate --remove-orphans