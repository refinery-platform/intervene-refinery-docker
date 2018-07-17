#!/bin/sh
set -e

python3 /usr/bin/parse.py --lists /tmp/fixtures/*.txt --output /tmp

# Make sure the directory for individual app logs exists
mkdir -p /var/log/shiny-server
chown shiny.shiny /var/log/shiny-server

exec shiny-server 2>&1