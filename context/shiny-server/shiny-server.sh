#!/bin/sh

python3 /tmp/python/parse.py --files /tmp/fixtures/*.txt --output /tmp

# Make sure the directory for individual app logs exists
mkdir -p /var/log/shiny-server
chown shiny.shiny /var/log/shiny-server

exec shiny-server 2>&1