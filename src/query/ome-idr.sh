#!/bin/bash

SOURCE_PREFIX=https://ftp.ebi.ac.uk/pub/databases/IDR/idr0086-miron-micrographs/20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed/
XY_DATA_NAME=Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy
XZ_DATA_NAME=Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz
EXT=.tif

XY_DATA_FILE=$XY_DATA_NAME$EXT
XZ_DATA_FILE=$XZ_DATA_NAME$EXT


echo SOURCE_PREFIX$XY_DATA_FILE

# download data
curl -O $SOURCE_PREFIX$XY_DATA_FILE