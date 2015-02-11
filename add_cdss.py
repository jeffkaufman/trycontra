import urllib2
import json
import re

CDSS_URL="http://map.cdss.org/dances.human.json"
MAPPING_FILE="cdss_tc_mapping.txt"
EXCLUSIONS_FILE="cdss_exclusions.txt"

def slurp(url, data=None, timeout=60):
    headers = {'User-Agent': 'syncing bot by Jeff Kaufman (trycontra.com)'}
    return urllib2.urlopen(urllib2.Request(url, data, headers), None, timeout).read()

def near(lat1, lng1, lat2, lng2):
  return (lat1-lat2)*(lat1-lat2) + (lng1-lng2)*(lng1-lng2) < 0.02

def cannonical_url(url):
    if url.endswith("/"):
        return url[:-1]
    return url

def handle_dance(cdss_id, lat, lng, address, website, existing, mapping):
  if cdss_id in mapping:
      return

  for e_website, e_address, e_schedule, e_freq, e_lat, e_lng in existing:
      if near(lat, lng, e_lat, e_lng):
          add = False
          if cannonical_url(e_website) == cannonical_url(website) and e_address == address:
              print "Automatically accepting match for", address, website
              add = True
          else:
              print "potential_match:"
              print "   tc:", e_address, e_website, e_schedule, e_freq, e_lat, e_lng
              print " cdss:", address, website, lat, lng
              print "do they match?"
              if raw_input("y/n > ") == "y":
                  add = True
          if add:
              with open(MAPPING_FILE, "a") as outf:
                  outf.write("%s %s\n" % (cdss_id, e_website))
              return

  print "Consider adding to dances.json:"
  print "  lat:", lat
  print "  lng:", lng
  print "  adr:", address
  print "  url:", website
  print "Added?"
  if raw_input("y/n > ") == "y":
      with open(MAPPING_FILE, "a") as outf:
          outf.write("%s %s\n" % (cdss_id, website))
  else:
      with open(EXCLUSIONS_FILE, "a") as outf:
          outf.write("%s\n" % cdss_id)

def start():
    existing = json.loads(open("dances_locs.json").read())

    mapping = {}
    with open(MAPPING_FILE) as inf:
        for line in inf:
            line = line.strip().split()
            if line:
                cid, url = line
                mapping[cid] = url

    exclusions = []
    with open(EXCLUSIONS_FILE) as inf:
        for line in inf:
            exclusions.append(line.strip())

    r = json.loads(slurp(CDSS_URL))
    for dance in r:
        cdss_id = str(dance["id"])
        if cdss_id in exclusions:
            continue

        dance = dance["dance"]
        lat = dance["latitude"]
        lng = dance["longitude"]

        if "contra" in dance["dance_type"]:
            a = re.findall(", ([^,]+, [A-Z][A-Z]) [0-9]{5}, USA$", dance["approx_address"])
            if a:
                address = a[0].replace(",", "")
                # just take the first organizer
                website = dance["organizers"][0]["website"]

                handle_dance(cdss_id, lat, lng, address, website, existing, mapping)

if __name__ == "__main__":
    start()
