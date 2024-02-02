#!/usr/bin/env python3

import json
from collections import defaultdict

newest_year = -1
event_years = defaultdict(set) # name -> years
urls = {}

with open("events.json") as inf:
  for record in json.load(inf):
    event_years[record["name"]].add(record["year"])
    newest_year = max(record["year"], newest_year)
    urls[record["name"], record["year"]] = record["url"]
    
for event, years in event_years.items():
  if newest_year - 1 in years:
    if newest_year not in years:
      print(event, ", ".join(str(x) for x in sorted(years)))
    #else:
    #  if urls[event, newest_year] != urls[event, newest_year - 1]:
    #    print(event, urls[event, newest_year - 1], urls[event, newest_year])
      
    
    
