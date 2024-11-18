#!/usr/bin/env python3

import json
from collections import Counter, defaultdict

with open("events.json") as inf:
    events = json.load(inf)

year_gender_pair_counts = defaultdict(Counter)

female_first_names = [
    "Abigail",
    "Adina",
    "Andrea",
    "Anne",
    "Anna",
    "Barbara",
    "Beth",
    "Bev",
    "Beverly",
    "Brenda",
    "Brooke",
    "Carol",
    "Cathy",
    "Casey",
    "Charlotte",
    "Chrissy",
    "Christa",
    "Christine",
    "Cis",
    "Claire",
    "Dana",
    "Darlene",
    "Deanna",
    "Deb",
    "Dela",
    "Donna",
    "Diane",
    "Eileen",
    "Emily",
    "Frannie",
    "Gaye",
    "Gaile",
    "Georges",
    "Hannah",
    "Heather",
    "Jacqui",
    "Janet",
    "Janine",
    "Jean",
    "Jill",
    "Joanna",
    "Jolaine",
    "Jo",
    "Judy",
    "Kalia",
    "Karin",
    "Kathryn",
    "Kathy",
    "Katie",
    "Kate",
    "Katy",
    "Kelsey",
    "Kirsty",
    "Koren",
    "Kristen",
    "Lauren",
    "Linda",
    "Lindsey",
    "Lisa",
    "Liz",
    "Lynne",
    "Louise",
    "Lynn",
    "Mae",
    "Maggie",
    "Maia",
    "Mary",
    "Meg",
    "Miriam",
    "Nikki",
    "Nedra",
    "Noralyn",
    "Quena",
    "Rachel",
    "Rebecca",
    "Rhianwen",
    "River",
    "Robin",
    "Rhodri",
    "Roni",
    "Sarah",
    "Sue",
    "Susan",
    "Sylvie",
    "Shari",
    "Terry",
    "Tina",
    "Vicki",
    "Wendy",
]

male_first_names = [
    "Andrew",
    "Andy",
    "Barry",
    "Beau",
    "Ben",
    "Bill",
    "Bob",
    "Bradley",
    "Brian",
    "Bruce",
    "Cary",
    "Charlie",
    "Chuck",
    "Chet",
    "Chris",
    "Dan",
    "Dudley",
    "Donald",
    "Dave",
    "David",
    "Derek",
    "Dereck",
    "Devin",
    "Dugan",
    "Ed",
    "Erik",
    "Frank",
    "George",
    "Isaac",
    "Jeremy",
    "Jesse",
    "Jerome",
    "Jim",
    "Joe",
    "John",
    "Joseph",
    "Josiah",
    "Jonathan",
    "Kappy",
    "Larry",
    "Luke",
    "Michael",
    "Max",
    "Mark",
    "Nils",
    "Noah",
    "Owen",
    "Paul",
    "Peter",
    "Pop",
    "Rick",
    "Ridge",
    "Rob",
    "Roger",
    "Ron",
    "Roy",
    "Scott",
    "Scot",
    "Seth",
    "Shawn",
    "Steve",
    "Ted",
    "Tod",
    "Todd",
    "Tom",
    "Tim",
    "Timothy",
    "Tavi",
    "Tony",
    "Thos",
    "Warren",
    "Will",
    "Yoyo",
]

genders = {
    "Alex Deis-Lauby": "w",
    "Alex Cumming": "m",
    "Angela DeCarlis": "n",
    "Beadle": "m",
    "Charley Harvey": "m",
    "Julian Blechner": "n",
    "Laurel Thomas": "w",
    "Laurie Pietravalle": "w",
    "Lo Peckman": "w",
    "Rab Cummings": "m",
    "Sam Tetley Smith": "m",
}
    

for female_name in female_first_names:
    assert female_name not in male_first_names

for male_name in male_first_names:
    assert male_name not in female_first_names
            
def gender(name):
    g = genders.get(name)
    if g:
        return g

    first_name = name.split()[0]
    if first_name in female_first_names:
        return "w"
    if first_name in male_first_names:
        return "m"
    raise Exception("Uncategorized name %r" % name)

possible_mw_events = defaultdict(list)
for event in events:
    event_name = event["name"]
    if event_name.startswith("Dancing Fish"):
        event_name = "Dancing Fish"
    if len(event["callers"]) == 2:
        possible_mw_events[event_name].append(event["year"])

mw_event_bookings = defaultdict(dict)

for event in events:
    event_name = event["name"]
    if event_name.startswith("Dancing Fish"):
        event_name = "Dancing Fish"
    if len(event["callers"]) == 2:
        if "TBD" in event["callers"] or "Open Calling" in event["callers"]:
            continue

        event_genders = [gender(caller) for caller in event["callers"]]
        event_genders = "".join(sorted(event_genders))

        if event_name in possible_mw_events:
            if event_genders != "mw":
                del possible_mw_events[event_name]
                if event_name in mw_event_bookings:
                    del mw_event_bookings[event_name]
            else:
                mw_event_bookings[event_name][event["year"]] = event["callers"]
        if "n" in event_genders:
            continue
        
        year_gender_pair_counts[event["year"]][event_genders] += 1

if False:
    print("year", "mm", "mw", "ww", sep="\t")
    for year, gender_pair_counts in sorted(year_gender_pair_counts.items()):
        print(year, gender_pair_counts["mm"],
              gender_pair_counts["mw"],
              gender_pair_counts["ww"], sep="\t")
if False:
    for event_name in possible_mw_events:
        event_bookings = mw_event_bookings[event_name]
        if len(event_bookings) > 3:
            print(event_name)
            for year, callers in sorted(event_bookings.items()):
                print(" ", year, " and ".join(callers))

year_genders = defaultdict(Counter)
for event in events:
    for caller in event["callers"]:
        if caller in ["TBD", "Open Calling", "various", "open calling",
                      "Squash Family Callers", "not listed", "lots",
                      "Open calling",
                      "Squash Family and Cousins", "unnamed"]:
            continue
        print(caller)
        year_genders[event["year"]][gender(caller)] += 1

if False:
    for year, gender_counts in sorted(year_genders.items()):
        print("%s\t%.0f%%" % (
            year, 100.0 * gender_counts["w"] / (
                gender_counts["w"] + gender_counts["m"])))

year_single_genders = defaultdict(Counter)
for event in events:
    if len(event["callers"]) == 1:
        caller, = event["callers"]
        if caller in ["TBD", "Open Calling", "various", "open calling",
                      "Squash Family Callers", "not listed", "lots",
                      "Open calling",
                      "Squash Family and Cousins", "unnamed"]:
            continue
        year_single_genders[event["year"]][gender(caller)] += 1

if False:
    for year, gender_counts in sorted(year_single_genders.items()):
        print("%s\t%.0f%%" % (
            year, 100.0 * gender_counts["w"] / (
                gender_counts["w"] + gender_counts["m"])))

