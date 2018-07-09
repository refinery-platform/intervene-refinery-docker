#!/usr/bin/env bash
set -o errexit

source shared.sh

echo "REPO: $REPO"
echo "IMAGE: $IMAGE"

# TODO: docker pull $REPO

# TODO: --cache-from $REPO \
docker build \
       --tag $IMAGE \
       context