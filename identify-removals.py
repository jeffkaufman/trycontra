#!/usr/bin/env python3

import json
from collections import defaultdict

with open("events.json") as inf:
    all_events = json.load(inf)

max_year = max(event["year"] for event in all_events)
prev_year = max_year - 1

events_by_name_and_year = defaultdict(dict)
for event in all_events:
    if event["year"] not in [max_year, prev_year]:
        continue
    events_by_name_and_year[event["name"]][event["year"]] = event

for name in sorted(events_by_name_and_year):
    if len(events_by_name_and_year[name]) == 2:
        continue
    
    if max_year in events_by_name_and_year[name]:
        print("Added: %s" % name)
    if prev_year in events_by_name_and_year[name]:
        print("Removed: %s" % name)
