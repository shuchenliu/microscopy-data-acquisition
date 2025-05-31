#!/bin/bash

STORAGE_PROTOCOL=s3
TARGET_BUCKET=janelia-cosem-datasets
TARGET_DIRECORY=jrc_mus-nacc-2



# Data nature: large number of files
# Utilize s5cmd built-in worker pool for latency-bound tasks like this


s5cmd --no-sign-request cp --sp "$STORAGE_PROTOCOL://$TARGET_BUCKET/$TARGET_DIRECORY/*" .