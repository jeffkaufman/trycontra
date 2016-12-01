import sys
import json
import csv

def start(zip_csv):
  data = {}
  with open(zip_csv, 'rb') as inf:
    for i, row in enumerate(csv.reader(inf)):
      zipcode = row[0]
      lat = row[12]
      lng = row[13]

      if i == 0:
        assert zipcode == "zip"
        assert lat == "latitude"
        assert lng == "longitude"
      else:
        data[zipcode] = [float(lat), float(lng)]
  with open("zipcode.json", 'w') as outf:
    outf.write(json.dumps(data).replace("],", "],\n"))

if __name__ == "__main__":
  start(*sys.argv[1:])
