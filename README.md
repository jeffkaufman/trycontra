# TryContra

This is the source code and database backing https://trycontra.com

## Submitting Changes

Either send an email to Jeff (jeff@jefftk.com) or send a Pull Request.

If you're making a pull request, the process is:

1. Update `dances.json` with your change.

   Note that annual frequencies are just guesses based on looking at
   the website.

2. Run `./lookup_locs.py` to update `dances_locs.json` with your
   changes and pull in latitude and longitude.

3. Commit your changes and make a PR.

## Structure

* `index.html`: main page, containing both the display and the scripts.
* `dances.json`: dance database.
* `dances_locs.json`: dance database with locations automatically added.
* `zipcode.json`: giant map from zipcode to lat/lng.

## Updating `zipcode.json`

You can get the initial CSV from anywhere, but I found this one easy:
http://www.unitedstateszipcodes.org/zip-code-database/

Once you have the `.csv` you can run:

    python build_zipcode_json.py <csv-file>
