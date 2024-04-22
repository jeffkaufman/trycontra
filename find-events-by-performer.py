#!/usr/bin/env python3

import sys
import json

performer, = sys.argv[1:]

with open("events.json") as inf:
    events = json.load(inf)

years = set()
for event in events:
    if performer in event["bands"] or performer in event["callers"]:
        years.add(event["year"])

print(*sorted(years))
