#!/usr/bin/env bash
set -o errexit

source shared.sh

export INPUT_JSON="$(cat context/fixtures/food/fake-input.json)"
echo 'INPUT_JSON:'
echo $INPUT_JSON

docker run --env INPUT_JSON \
           --name "$CONTAINER_NAME" \
           --detach \
           --publish "$PORT:80" \
           $IMAGE
echo "Visit http://localhost:$PORT"