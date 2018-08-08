#!/bin/sh
set -e

echo 'environment:'
env # To help with debugging: Did we get the variables we expected?
echo

python3 /usr/bin/main.py \
    --json /tmp/input.json \
    --output /srv/shiny-server/sample-apps/intervene/data

# Make sure the directory for individual app logs exists
mkdir -p /var/log/shiny-server
chown shiny.shiny /var/log/shiny-server

exec shiny-server 2>&1