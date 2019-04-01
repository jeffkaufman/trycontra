from collections import defaultdict
import json
import math

dances = []
with open("dances_locs.json") as inf:
  for url,_,_,_,lat,lng,_ in json.loads(inf.read()):
    dances.append((url, (lat,lng)))

zips = {}
with open("zipcode.json") as inf:
  zips = json.loads(inf.read())

def distancesq(lat1, lng1, lat2, lng2):
  # Approximate a flat Earth at the average latitude.
  dlat = lat1 - lat2
  dlng = (lng1 - lng2) * math.cos(0.5*(lat1 + lat2) * math.pi / 180.0)
  return dlat*dlat + dlng*dlng

def closest_dance(lat, lng):
  so_far_loc = None
  so_far_dist = None
  so_far_url = None
  for url, loc in dances:
    #print ("    considering %s at %s" % (url, loc))
    dist = distancesq(lat, lng, *loc)
    if not so_far_dist or dist < so_far_dist:
      #print("      accepted %s with dist %s from %s" % (url, dist, loc))
      so_far_loc = loc
      so_far_dist = dist
      so_far_url = url
  return so_far_url

def determine_prefixes(prefix_size):
  print ("determining prefixes at size %s" % prefix_size)
  counts = defaultdict(int)
  lats = defaultdict(float)
  lngs = defaultdict(float)

  for zipcode, (lat, lng) in zips.items():
    prefix = zipcode[:prefix_size]
    counts[prefix] += 1
    lats[prefix] += lat
    lngs[prefix] += lng

  prefix_average = {}
  for prefix, count in counts.items():
    prefix_average[prefix] = lats[prefix]/count, lngs[prefix]/count

  return prefix_average

prefix_averages = {
  prefix_size: determine_prefixes(prefix_size)
  for prefix_size in [1,2,3,4]}

def pick_prefix_size(zipcode):
  print("picking prefix size for %s" % zipcode)
  closest_url = closest_dance(*zips[zipcode])
  print("  want to keep %s" % closest_url)
  for prefix_size in reversed(sorted(prefix_averages)):
    print("  considering size %s" % prefix_size)
    candidate_url = closest_dance(
      *prefix_averages[prefix_size][zipcode[:prefix_size]])
    print("    would give %s" % candidate_url)
    if candidate_url != closest_url:
      return prefix_size + 1  # too far, back up one
  return 1

final = {}
for zipcode in sorted(zips):
  prefix_size = pick_prefix_size(zipcode)
  prefix = zipcode[:prefix_size]
  print("  chose %s" % prefix)
  if prefix_size == 5:
    loc = zips[zipcode]
  else:
    loc = prefix_averages[prefix_size][prefix]
    
  final[prefix] = loc

with open("zipcomp2.json", "w") as outf:
  outf.write("{\n")
  for prefix in sorted(final):
    outf.write('  "%s": [%.2f, %.2f]"\n' % (
      prefix, *final[prefix]))
  outf.write("}\n")
