#!/usr/bin/env python3

import sys
import json

caller, = sys.argv[1:]

with open("events.json") as inf:
    for record in json.load(inf):
        date = record["date"]
        if not date:
            continue

        mm, dd, yyyy = date.split("/")

        date = "%s-%s-%s" % (yyyy, mm, dd)

        if caller in record["callers"]:
            print(date, record["name"])
