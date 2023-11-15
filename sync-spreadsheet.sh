#!/usr/bin/env bash

# Usage: ./sync-spreadsheet.sh <Google Sheet key>
# The Google Sheet key is a 44-character long alphanumeric string which you can get from the URL of
# the spreadsheet.

set -e

git pull

for i in 2017 2018 2019 2023 2024; do
    wget "https://docs.google.com/spreadsheets/d/$1/gviz/tq?tqx=out:csv&sheet=$i" -O - \
    | csvformat -T > events-raw-$i.tsv
    unix2dos events-raw-$i.tsv
done

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    ./process-events.py
    ./lookup_locs.py

    git commit events-raw-*.tsv events.json -m "sync with spreadsheet"
    git push
fi
