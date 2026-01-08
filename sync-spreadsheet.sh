#!/usr/bin/env bash

# Usage: ./sync-spreadsheet.sh

set -e
set -o pipefail

git pull

declare -A sheet_gids=(
#    ["2016"]="1649588387"
#    ["2017"]="602090070"
#    ["2018"]="1899461454"
#    ["2019"]="1075288908"
#    ["2023"]="39088556"
#    ["2024"]="53541576"
    ["2025"]="1187858755"
    ["2026"]="465816395"
    ["2027"]="1232069085"
)


sheet_key="1fQq7pTtNVMYVRgOPbjNz2jnyw4RABGrQoplrSQntbn8"
url="https://docs.google.com/spreadsheets/d/${sheet_key}/export?format=csv"

for year in "${!sheet_gids[@]}"; do
    gid="${sheet_gids[$year]}"

    echo "Downloading sheet $year (gid: $gid)..."
    curl -L -sS "$url&gid=${gid}" | csvformat -T > "events-raw-$year.tsv"
done

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    ./process-events.py
    ./lookup_locs.py

    git commit events-raw-*.tsv events.json -m "sync with spreadsheet"
    git push

    git icdiff HEAD~1
fi
