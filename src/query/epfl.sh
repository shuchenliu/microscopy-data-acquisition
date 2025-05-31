#!/bin/bash

# define data source
DATA_FILE=https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif

# Data nature: single large file
# utilize aria2c multi-connection / multi-part support for files of larger sizes
aria2c -x 20 $DATA_FILE
