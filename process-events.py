#!/usr/bin/env python3
import re
import glob
import json
from collections import Counter, defaultdict
from difflib import SequenceMatcher

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

name_changes = {
    'Wendy Graham Settle': 'Wendy Graham',
    'Lauren Peckman': 'Lo Peckman',
    'Ron Blechner': 'Julian Blechner',
    'River Rainbowface Abel': 'River Rainbowface',
    'River Abel': 'River Rainbowface',
    'Emily Abel': 'River Rainbowface',
}

possible_the_bands = set()

all_bands_ever = Counter()
all_callers_ever = Counter()
band_years = defaultdict(set)
caller_years = defaultdict(set)

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

            bands = [name_changes.get(band, band) for band in bands]
            callers = [name_changes.get(caller, caller) for caller in callers]

            for band in bands:
                all_bands_ever[band] += 1
                band_years[band].add(year)
            for caller in callers:
                all_callers_ever[caller] += 1
                caller_years[caller].add(year)

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

# Flag typos for human review, where there are multiple entries in
# all_bands_ever (or all_callers_ever) that look suspiciously similar to each
# other.  Generated by Claude 3.7.
def detect_possible_typos(counter, similarity_threshold=0.85 , min_count=1):
    """
    Detect possible typos in names by finding pairs with high similarity.

    Args:
        counter: Counter object containing name frequencies
        similarity_threshold: Threshold for considering names similar (0.0-1.0)
        min_count: Minimum count to consider for reporting

    Returns:
        List of tuples (name1, count1, name2, count2, similarity)
    """
    possible_typos = []
    items = list(counter.items())

    for i in range(len(items)):
        name1, count1 = items[i]
        if count1 < min_count:
            continue

        for j in range(i+1, len(items)):
            name2, count2 = items[j]
            if count2 < min_count:
                continue

            # Skip exact matches (case insensitive)
            if name1.lower() == name2.lower():
                continue

            # Calculate similarity
            similarity = SequenceMatcher(None, name1.lower(),
            name2.lower()).ratio()

            # Check for high similarity
            if similarity >= similarity_threshold:
                possible_typos.append((name1, count1, name2, count2,
                similarity))

    # Sort by similarity (highest first)
    return sorted(possible_typos, key=lambda x: x[4], reverse=True)

for performer_type, all_ever, all_years in [
        ("band", all_bands_ever, band_years),
        ("caller", all_callers_ever, caller_years),
]:
    typos = detect_possible_typos(all_ever)
    if not typos:
        continue

    print("\nPossible %s typos:" % performer_type)
    for name1, count1, name2, count2, similarity in typos:
        name_1_years = ", ".join(str(x) for x in sorted(all_years[name1]))
        name_2_years = ", ".join(str(x) for x in sorted(all_years[name2]))
        print(f"'{name1}' (used {count1}x: {name_1_years}) vs")
        print(f"'{name2}' (used {count2}x: {name_2_years})")
        print(f"Similarity: {similarity:.2f}\n")

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
