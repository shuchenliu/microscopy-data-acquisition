#!/bin/bash

STORAGE_PROTOCOL=s3
TARGET_BUCKET=janelia-cosem-datasets
TARGET_DIRECTORY=jrc_mus-nacc-2



# Data nature: large number of small files
# Utilize s5cmd built-in worker pool for latency-bound tasks

s5cmd --no-sign-request cp --sp "$STORAGE_PROTOCOL://$TARGET_BUCKET/$TARGET_DIRECTORY/*" .