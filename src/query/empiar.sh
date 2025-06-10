#!/bin/bash
#
# We could use Aspera CLI to sync file from EMPIAR
# but since this is relatively a smaller dataset (~1.2G)
# downloading a tarball from EMPIAR endpoint using a
# smaller 'hack' seems an easier way

DATA_DIR_NAME='empiar'

# output dir has to be created before data query
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../../data/$DATA_DIR_NAME"
mkdir -p "$OUTPUT_DIR" 2> /dev/null

EMPIAR_URI='https://www.ebi.ac.uk/empiar/EMPIAR-11759/'


# There are two things we'd need for query the compressed zip
# 1. the cooke, with csrf-token
# 2. the csrf-middleware-token, parsed from <div id='root-empiar-entry />
COOKIE_JAR=cookies.txt

TOKEN=$(curl -s $EMPIAR_URI -c $COOKIE_JAR \
  | grep -o 'csrf-token="[^"]*"' | cut -d'"' -f2)


# file IDs we'd need for the server to generate .zip
## smaller test ids
#PARENTS=$(echo {18464846..18464846} | tr ' ' '-')
PARENTS=$(echo {18464846..18465029} | tr ' ' '-')


# define output name
SAVED_FILE_NAME="empiar.tar"

curl 'https://www.ebi.ac.uk/empiar/EMPIAR-11759/get_zip/' \
  -X POST \
  -b cookies.txt \
  --data-raw "csrfmiddlewaretoken=$TOKEN&name=$SAVED_FILE_NAME&parents=$PARENTS" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Referer: https://www.ebi.ac.uk/empiar/EMPIAR-11759/' \
  --output-dir "$OUTPUT_DIR" \
  -o $SAVED_FILE_NAME \


# delete cookie file
rm $COOKIE_JAR

# unzip file
tar -xvf "$OUTPUT_DIR/$SAVED_FILE_NAME" -C "$OUTPUT_DIR/.."
rm "$OUTPUT_DIR/$SAVED_FILE_NAME"

