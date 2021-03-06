#!/bin/bash

set -e

HTML_FNAME=index.html
RECSCHEDULE_PDF=recschedule-latest.pdf
RECSCHEDULE_TXT=recschedule-latest.txt

current_date=`date`
echo === "$current_date" ===

curl -s http://web.mit.edu/athletics/www/recschedule.pdf -o $RECSCHEDULE_PDF
if [ "$(uname)" == "Darwin" ]; then
  md5_hash=$(md5 $RECSCHEDULE_PDF)
else
  md5_hash=$(md5sum $RECSCHEDULE_PDF)
fi

echo "Downloaded recschedule. $md5_hash"
pdftotext -layout $RECSCHEDULE_PDF $RECSCHEDULE_TXT

if python main.py $RECSCHEDULE_TXT $HTML_FNAME; then
  echo "Success! Wrote to $HTML_FNAME"
else
  cp $RECSCHEDULE_PDF recschedule-failed.pdf
  cp $RECSCHEDULE_TXT recschedule-failed.txt
  echo "Failure! Copied PDF/txt to recschedule-failed*"
fi
