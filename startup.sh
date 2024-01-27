#!/bin/bash

# this script is for the Dockerfile CMD

set -e

{ sleep 10; ./run_indexer.sh; } &

gunicorn --config etc/gunicorn_conf_rsp.py responder.app:app


# https://stackoverflow.com/questions/71063040/how-to-run-shell-command-after-gunicorn-service-this-is-for-docker-enterypoint

# https://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
