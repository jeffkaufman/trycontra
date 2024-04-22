#!/usr/bin/env python3

import sys
import json

year, = sys.argv[1:]
year = int(year)

printed = set()
with open("events.json") as inf:
    for event in json.load(inf):
        if event["year"] == year:
            url = event["url"]
            if url in printed:
                continue
            else:
                print(url)
                printed.add(url)


    
