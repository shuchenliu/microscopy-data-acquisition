#!/bin/bash

DATA_DIR_NAME='epfl'

# output dir has to be created before data query
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../../data/$DATA_DIR_NAME"
mkdir -p "$OUTPUT_DIR" 2> /dev/null

# define data source
DATA_FILE=https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif

# Data nature: single large file
# utilize aria2c multi-connection / multi-part support for files of larger sizes
aria2c -d "$OUTPUT_DIR" -x 16 $DATA_FILE
