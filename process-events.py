#!/usr/bin/env python3
import re
import json

bands_add_the = [
    'Adobe Brothers', 'Avant Gardeners', 'Canote Brothers',
    'Contrarians', 'Dam Beavers', 'Engine Room', 'Faux Paws',
    'Figments', 'Free Raisins', 'Gaslight Tinkers', 'JEMS',
    'Latter Day Lizards', 'Mean Lids', 'Moving Violations',
    "O'Schraves", 'Offbeats', 'Quarks',
    'Red Mountain Yellowhammers', 'Rhythm Raptors', 'Ripples',
    'Stringrays', 'Stuff', 'Syncopaths', 'Turning Stile', 'Whoots']

records = []
for year, fname in [
        (2016, "events-raw-2016.tsv"),
        (2017, "events-raw-2017.tsv"),
        (2018, "events-raw-2018.tsv"),
        (2019, "events-raw-2019.tsv"),
        (2023, "events-raw-2023.tsv"),
        (2024, "events-raw-2024.tsv"),
        (2025, "events-raw-2025.tsv"),
]:
    with open(fname) as inf:
        for n, line in enumerate(inf):
            if n == 0:
                continue

            if year <= 2023:
                (typical_month,
                 name,
                 caller1,
                 caller2,
                 caller3,
                 caller4,
                 caller5,
                 caller6,
                 band1,
                 band2,
                 band3,
                 band4,
                 band5,
                 band6,
                 roles,
                 date,
                 location,
                 url,
                 *_) = line.split("\t")
                date_end = ""
            else:
                (typical_month,
                 name,
                 caller1,
                 caller2,
                 caller3,
                 caller4,
                 caller5,
                 caller6,
                 band1,
                 band2,
                 band3,
                 band4,
                 band5,
                 band6,
                 roles,
                 date,
                 date_end,
                 location,
                 url,
                 *_) = line.split("\t")

            if not name:
                continue

            if name == "end of active list":
                break

            callers = [x for x in (caller1,
                                   caller2,
                                   caller3,
                                   caller4,
                                   caller5,
                                   caller6)
                       if x.strip()]

            bands = [re.sub("^The ", "the ", x)
                     for x in (band1,
                               band2,
                               band3,
                               band4,
                               band5,
                               band6)
                     if x.strip() and x.lower() != "unnamed"]

            bands = [
                "the " + band if band in bands_add_the else band
                for band in bands]

            rec = {
                "typical_month": typical_month,
                "name": name,
                "callers": callers,
                "bands": bands,
                "roles": roles,
                "date": date,
                "location": location,
                "url": url,
                "year": year,
            }
            if date_end:
                rec["date_end"] = date_end
            records.append(rec)

with open("events.json") as inf:
    old_records = json.load(inf)

loc_to_ll = {}
for record in old_records:
    if record.get("latlng","") and record.get("location", ""):
        loc_to_ll[record["location"]] = record["latlng"]

for record in records:
    if record.get("location", ""):
        if record["location"] in loc_to_ll:
            record["latlng"] = loc_to_ll[record["location"]]

with open("events.json", "w") as outf:
    json.dump(records, outf, indent=2)
