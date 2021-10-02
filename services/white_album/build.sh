#!/bin/bash
docker-compose -f docker-compose-build.yml up --build --remove-orphans --force-recreate
