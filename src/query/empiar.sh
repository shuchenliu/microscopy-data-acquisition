#!/bin/bash

EMPIAR_URI='https://www.ebi.ac.uk/empiar/EMPIAR-11759/'

# There are two things we'd need for query the compressed zip
# 1. the cooke, with csrf-token
# 2. the csrf-middleware-token, parsed from <div id='root-empiar-entry />
TOKEN=$(curl -s $EMPIAR_URI -c cookies.txt \
  | grep -o 'csrf-token="[^"]*"' | cut -d'"' -f2)


# file IDs we'd need for the server to generate .zip
#PARENTS=$(seq -s '-' 18464846 18465029 | tr ' ' '-')
PARENTS=$(echo {18464846..18464846} | tr ' ' '-')

# define output name
SAVED_FILE_NAME="empiar.zip"

curl 'https://www.ebi.ac.uk/empiar/EMPIAR-11759/get_zip/' \
  -X POST \
  -b cookies.txt \
  --data-raw "csrfmiddlewaretoken=$TOKEN&name=$SAVED_FILE_NAME&parents=$PARENTS" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.ebi.ac.uk/empiar/EMPIAR-11759/' \
  -o $SAVED_FILE_NAME # <-- This saves the output to a file


echo "Done! File saved as $SAVED_FILE_NAME"

