import json
import urllib2
import time

def lookup_ll(loc):
  loc = loc.replace(" ", "+")
  q = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % loc
  j = urllib2.urlopen(q).read()
  r = json.loads(j)

  try:
    ll = r["results"][0]["geometry"]["location"]
  except Exception:
    import pprint
    pprint.pprint(r)
    return 0,0

  return ll["lat"], ll["lng"]

def start():
  dances = json.loads(open("dances.json").read())
  loc_dances = []
  for url, loc, freq in dances:
    lat, lng = lookup_ll(loc)
    loc_dances.append([url, loc, freq, lat, lng])
    time.sleep(1)
  with open("dances_locs.json", "w") as outf:
    outf.write(json.dumps(loc_dances))

if __name__ == "__main__":
  start()
  
