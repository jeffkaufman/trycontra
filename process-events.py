#!/usr/bin/env python3
import re
import glob
import json

bands_add_the = [
    "O'Schraves",
    'Adobe Brothers',
    'Avant Gardeners',
    'Buzz Band',
    'Canote Brothers',
    'Cheap Shots',
    'Contra Rebels',
    'Contrarians',
    'Cosmic Otters',
    'Crabapples',
    'Dam Beavers',
    'Dead Sea Squirrels',
    'Dixie Butterhounds',
    'Dog Walkers',
    'Electrodes',
    'Engine Room',
    'FIgments',
    'Faux Paws',
    'Fiddle Hellions',
    'Figments',
    'Free Raisins',
    'Gaslight Tinkers',
    'Hat Band',
    'Hollertones',
    'Ice Cream Truckers',
    'JEMS',
    'Jig Lords',
    'Johns',
    'Latter Day Lizards',
    'Luddite Ramblers',
    'Mean Lids',
    'Midlings',
    'Moving Violations',
    'O-Tones',
    'Offbeats',
    'Old-Time Superstars',
    'Olympia Volunteer String Band',
    'Orphans',
    'Pegasus Collective',
    'Quarks',
    'Reckoners',
    'Red Mountain Yellowhammers',
    'Resurrection Marys',
    'Rhythm Raptors',
    'Ripples',
    'Sage Thrashers',
    'Sail Away Ladies',
    'Stringrays',
    'Stuff',
    'Syncopaths',
    'Tricky Brits',
    'Tune Drivers',
    'Turning Stile',
    'Virginia Creepers',
    'Whoots',
    'Yellow Dandies',
]

possible_the_bands = set()

records = []
for fname in sorted(glob.glob("events-raw-*.tsv")):
    year = int(fname.removeprefix("events-raw-").removesuffix(".tsv"))
    with open(fname) as inf:
        for n, line in enumerate(inf):
          try:
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

            for band in bands:
                if band.startswith("the ") and \
                   band.removeprefix("the ") not in bands_add_the:
                    possible_the_bands.add(band)

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

            if name == "continued":
                records[-1]["callers"].extend(callers)
                records[-1]["bands"].extend(bands)
            else:
                records.append(rec)
          except Exception:
            print(line)
            raise

if possible_the_bands:
    print("Consider adding to the 'bands_add_the' list:")
    for possible_the_band in sorted(possible_the_bands):
        print("    %r," % possible_the_band.removeprefix("the "))
        
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
