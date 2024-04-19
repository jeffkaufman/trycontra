#!/usr/bin/env python3

import json
from collections import defaultdict, Counter

# name -> gig list
callers = defaultdict(list)

def canonical(caller):
    caller = caller.lower().strip()
    if caller == "wendy graham":
        caller = "wendy graham settle"
    elif caller == "squash family and cousins":
        caller = "squash family callers"
    elif caller in ["river abel",
                    "river rainbowface"]:
        caller = "river rainbowface abel"
    
    

    if ("unnamed" in caller or
        "open" in caller or
        "various" in caller or
        "not listed" in caller or
        "tbd" in caller):
        return None
    
    return caller

years = set()
with open("events.json") as inf:
    for record in json.load(inf):
        date = record["date"]
        if not date:
            continue

        mm, dd, yyyy = date.split("/")
        years.add(yyyy)

        date = "%s-%s-%s" % (yyyy, mm, dd)
        
        for caller in record["callers"]:
            caller = canonical(caller)
            if caller:
                callers[caller].append((
                    date,
                    record["name"]))

for caller in callers:
    callers[caller].sort()


if False:
    for caller in sorted(callers):
        print(caller)

target_years = [year for year in sorted(years) if year >= "2018"]

fraction_by_threshold = []
for threshold in [1,2,3,4,5]:
    new_by_year = defaultdict(list)
    experienced_by_year = defaultdict(list)

    for caller in callers:
        previous = 0
        for date, gig in callers[caller]:
            year, _, _ = date.split("-")

            if previous >= threshold:
                experienced_by_year[year].append((caller, gig))
            else:
                new_by_year[year].append((caller, gig))

            previous += 1

    if False:
        for year in sorted(years):
            print(year, len(new_by_year[year]), len(experienced_by_year[year]),
                  "%.0f%%" % (100 * len(new_by_year[year]) / (
                      len(new_by_year[year]) +
                      len(experienced_by_year[year]))))

    row = []
    for year in target_years:
        row.append(len(new_by_year[year]) / (len(new_by_year[year]) +
                                             len(experienced_by_year[year])))
    print(threshold, *row, sep="\t")

if False:
    threshold = 1
    for caller in sorted(callers):
        previous = 0
        for date, gig in callers[caller]:
            year, _, _ = date.split("-")

            if previous < threshold and year in target_years:
                print(caller, year, gig, sep="\t")
                break
                
            previous += 1
