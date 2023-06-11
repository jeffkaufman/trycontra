#!/usr/bin/env python3
import json

records = []
with open("weekends-raw-2023.tsv") as inf:
    for n, line in enumerate(inf):
        if n == 0:
            continue

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

        bands = [x for x in (band1,
                             band2,
                             band3,
                             band4,
                             band5,
                             band6)
                 if x.strip()]

        
        records.append(
            {"typical_month": typical_month,
             "name": name,
             "callers": callers,
             "bands": bands,
             "roles": roles,
             "date": date,
             "location": location,
             "url": url,
             }
        )

with open("weekends.json", "w") as outf:
    json.dump(records, outf)
