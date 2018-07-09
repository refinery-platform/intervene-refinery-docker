#!/usr/bin/env bash
set -o errexit

source shared.sh

docker run --env INPUT_JSON_URL='https://raw.githubusercontent.com/refinery-platform/shiny-docker-demo/v0.0.1/fixtures/fake-input.json' \
           --name $CONTAINER_NAME \
           --detach \
           --publish $PORT:80 \
           $IMAGE
echo "Visit http://localhost:$PORT"