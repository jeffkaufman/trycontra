#!/usr/bin/env python3

import json
from json import encoder
import requests
import urllib.parse
import time

KEY="AIzaSyCuMCzvNjdpzYJMFR8BWmbGzO68HbHPkGA"

#force ipv4
import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
  responses = old_getaddrinfo(*args, **kwargs)
  return [response
          for response in responses
          if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

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
  existing_locs = json.loads(open("dances_locs.json").read())
  loc_lookup = {}

  for url, loc, days, freq, lat, lng, *rest in existing_locs:
    loc_lookup[loc] = [lat, lng]
  return loc_lookup

def start():
  dances = json.loads(open("dances.json").read())
  loc_lookup = build_loc_lookup()

  loc_dances = []
  for row in dances:

    try:
      url, loc, days, freq, roles, active = row
    except Exception:
      print(row)
      raise

    if roles not in ["GF", ""]:
      raise Exception("unknown roles %r in %r" % (
        roles, line))

    if '(' in loc:
      lat, lng = None, None
    elif loc in loc_lookup:
      lat, lng = loc_lookup[loc]
    else:
      lat, lng = lookup_ll(loc)
      time.sleep(1)
    loc_dances.append([url, loc, days, freq, lat, lng, roles, active])
  with open("dances_locs.json", "w") as outf:
    outf.write(json.dumps(loc_dances).replace("],", "],\n"))

  with open("events.json") as inf:
    event_records = json.load(inf)

  for event_record in event_records:
    if event_record["location"] and "latlng" not in event_record:
      event_record["latlng"] = lookup_ll(event_record["location"])

  with open("events.json", "w") as outf:
    json.dump(event_records, outf)

if __name__ == "__main__":
  start()
