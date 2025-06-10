#!/bin/bash

DATA_DIR_NAME='jrc_mus-nacc-2'

# output dir has to be created before data query
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../../data/$DATA_DIR_NAME"
mkdir -p "$OUTPUT_DIR" 2> /dev/null

# remote location config
STORAGE_PROTOCOL=s3
TARGET_BUCKET=janelia-cosem-datasets
TARGET_DIRECTORY=jrc_mus-nacc-2



# Data nature: large number of small files
# Utilize s5cmd built-in worker pool for latency-bound tasks

s5cmd --no-sign-request cp --sp "$STORAGE_PROTOCOL://$TARGET_BUCKET/$TARGET_DIRECTORY/*" "$OUTPUT_DIR"