#!/usr/bin/env bash
git pull

any_changed=false
for i in {2000..2100}; do
    in_fname=~/Downloads/Dance\ Weekends,\ Festivals,\ and\ Long\ Dances\ -\ $i.tsv
    if [ -e "$in_fname" ] ; then
        mv "$in_fname" events-raw-$i.tsv
        any_changed=true
    fi
done
if $any_changed; then
    ./process-events.py
    ./lookup_locs.py
    git commit events-raw-*.tsv events.json -m "sync with spreadsheet"
    git push
fi


