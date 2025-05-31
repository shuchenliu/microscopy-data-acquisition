#!/bin/bash

# define data source
DATA_FILE=https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/%20ElectronMicroscopy_Hippocampus/volumedata.tif

# utilize aria2c multi-connection support for files of larger sizes
aria2c -x 8 $DATA_FILE
