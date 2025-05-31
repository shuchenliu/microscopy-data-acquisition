#!/bin/bash

SOURCE_PREFIX=https://ftp.ebi.ac.uk/pub/databases/IDR/idr0086-miron-micrographs/20200610-ftp/experimentD/Miron_FIB-SEM/Miron_FIB-SEM_processed/
XY_DATA_NAME=Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xy
XZ_DATA_NAME=Figure_S3B_FIB-SEM_U2OS_20x20x20nm_xz
EXT=.tif

XY_DATA_FILE=$XY_DATA_NAME$EXT
XZ_DATA_FILE=$XZ_DATA_NAME$EXT


# utilize curl non-blocking I/O for files smaller sizes
curl -Z -O $SOURCE_PREFIX$XY_DATA_FILE -O $SOURCE_PREFIX$XZ_DATA_FILE