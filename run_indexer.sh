#!/bin/bash

# if desired, run thusly to see extra output:
# BFG_ENV=DEV ./run_indexer.sh

echo "Starting firehose at $(date) ..."

python -c "
import indexer.application
indexer.application.application()
"
