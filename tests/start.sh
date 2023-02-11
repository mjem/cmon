#!/bin/bash

# Start a small demo network of services for use with the demo_config.py cmon configuration file
# Requires the docker damon to already be running and current user has permissions to control it

docker-compose -f tests/docker-compose.yaml up -d
