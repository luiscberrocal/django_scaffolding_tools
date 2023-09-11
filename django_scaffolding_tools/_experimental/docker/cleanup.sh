#! /usr/bin/bash

# read -p 'Regula expression: ' REGEXP
REGEXP=payment-collector

echo Filtering for $REGEXP
# docker ps -a | grep  -E $REGEXP
d-stop
docker ps -a | grep  -E $REGEXP | awk '{print $1}' | xargs docker rm
docker volume ls |  grep -E $REGEXP | awk '{print $2}' | xargs docker volume rm
docker image ls | grep -E $REGEXP | xargs docker image rm
