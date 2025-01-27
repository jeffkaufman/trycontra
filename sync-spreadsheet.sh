#!/usr/bin/env bash

# Usage: ./sync-spreadsheet.sh

set -e

git pull

sheet_key="1fQq7pTtNVMYVRgOPbjNz2jnyw4RABGrQoplrSQntbn8"
sheet_url="https://docs.google.com/spreadsheets/d/$sheet_key/gviz/tq?tqx=out:csv"
for i in 2016 2017 2018 2019 2023 2024 2025; do
    curl -sS "${sheet_url}&sheet=$i" | csvformat -T > events-raw-$i.tsv
done

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    ./process-events.py
    ./lookup_locs.py

    git commit events-raw-*.tsv events.json -m "sync with spreadsheet"
    git push

    git icdiff HEAD~1
fi
