#!/usr/bin/env python3

import json
import sys
from json import encoder
import requests
import urllib.parse
import time
from private import KEY

#force ipv4
import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
  responses = old_getaddrinfo(*args, **kwargs)
  return [response
          for response in responses
          if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

# How much of an over-long line to show around the error, and how many
# lines of leading context to print.
WINDOW = 100
CONTEXT_LINES = 2

def load_json(fname):
  with open(fname) as inf:
    contents = inf.read()

  try:
    return json.loads(contents)
  except json.JSONDecodeError as e:
    sys.stderr.write("%s: %s at line %s column %s:\n\n" % (
      fname, e.msg, e.lineno, e.colno))

    lines = contents.split("\n")

    # How far along the line the caret goes, once tabs are expanded.
    caret_col = len(lines[e.lineno - 1][:e.colno - 1].expandtabs())

    # Long lines get windowed so the offending character stays visible.
    start = 0
    if caret_col > WINDOW - 20:
      start = caret_col - (WINDOW - 20)

    def show(line):
      line = line.expandtabs()[start:]
      if start and line:
        line = "..." + line
      if len(line) > WINDOW:
        line = line[:WINDOW] + "..."
      return line

    for lineno in range(max(1, e.lineno - CONTEXT_LINES), e.lineno + 1):
      sys.stderr.write("%6d | %s\n" % (lineno, show(lines[lineno - 1])))
    sys.stderr.write("%6s | %s^\n" % (
      "", " " * (caret_col - start + (3 if start else 0))))

    sys.exit(1)

def lookup_ll(loc):
  print ("looking up %s" % loc)
  loc = urllib.parse.quote_plus(loc)
  q = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (loc, KEY)

  print(q)
  response = requests.get(q)
  print(response)
  r = response.json()

  try:
    ll = r["results"][0]["geometry"]["location"]
  except Exception:
    import pprint
    pprint.pprint(r)
    raise

  return round(ll["lat"], 2), round(ll["lng"], 2)

def build_loc_lookup():
  existing_locs = load_json("dances_locs.json")
  loc_lookup = {}

  for record in existing_locs:
    loc_lookup[record["city"]] = record["lat"], record["lng"]
  return loc_lookup

def start():
  dances = load_json("dances.json")
  loc_lookup = build_loc_lookup()

  loc_dances = []
  for record in dances:
    loc = record["city"]
    if '(' in loc:
      lat, lng = None, None
    elif loc in loc_lookup:
      lat, lng = loc_lookup[loc]
    else:
      lat, lng = lookup_ll(loc)
      time.sleep(1)

    record["lat"] = lat
    record["lng"] = lng
    
  with open("dances_locs.json", "w") as outf:
    json.dump(dances, outf, sort_keys=True, indent=2)

  event_records = load_json("events.json")

  for event_record in event_records:
    if event_record["location"] and "latlng" not in event_record:
      event_record["latlng"] = lookup_ll(event_record["location"])

  with open("events.json", "w") as outf:
    json.dump(event_records, outf, indent=2)

if __name__ == "__main__":
  start()
