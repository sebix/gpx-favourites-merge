#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:13:02 2019

@author: sebastianw

TODO: Drop exact duplicates
"""

import csv
import glob
import xmltodict

filenames = glob.glob("/home/sebastianw/Downloads/gpxmerge/*.gpx")
#filenames = glob.glob("/home/sebastianw/Downloads/gpxmerge/tablet.gpx")

data = []
for filename in filenames:
    with open(filename) as handle:
        data.extend(xmltodict.parse(handle.read())['gpx']['wpt'])

data = sorted(data, key=lambda x: float(x['@lat']) + float(x['@lon']))
#fieldnames = set()
#for x in data:
#    fieldnames.update(set(x.keys()))
fieldnames = ['@lat', '@lon', 'name', 'cmt', 'desc', 'type']

colors = {'Sightseeing': '#b400842b',
 'Travel': '#b4e044bb',
 'Friends': '#b4eeee10',
 'Transport': '#b4d00d0d',
 'Tankstellen': '#b48e2512',
 'Shops': '#b488e030',
 'Work': '#b410c0f0',
 'Uni': '#b400842b',
 'Wanderung': '#b400842b',
 'Waypoints': '#b4ff5020',
 'Customers': '#b410c0f0',
 'TODO': '#000000',
 'Restaurant': '#000000'}

def write_csv():
    with open("/home/sebastianw/Downloads/gpxmerge/tablet.csv", 'w') as out:
        writer = csv.DictWriter(out, fieldnames)
        writer.writeheader()
        writer.writerows(data)

def read_csv():
    with open("/home/sebastianw/Downloads/gpxmerge/out.csv") as handle:
        return list(csv.DictReader(handle))

categories = {}
def read_categories():
    for wpt in data:
        if 'extensions' not in wpt:
            continue
        categories[wpt['type']] = wpt['extensions']['color']

def write_gpx():
    with open("/home/sebastianw/Downloads/gpxmerge/gpxout", 'w') as handle:
        handle.write("""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<gpx version="1.1" creator="OsmAnd+ 3.4.8" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>favourites</name>
  </metadata>
""")
        for wpt in data:
            handle.write(f"""  <wpt lat="{wpt['@lat']}" lon="{wpt['@lon']}">
    <name>{wpt['name']}</name>
    <type>{wpt['type']}</type>
    <cmt>{wpt['cmt']}</cmt>
    <extensions>
      <color>{colors[wpt['type']]}</color>
    </extensions>
  </wpt>\n""")
        handle.write('</gpx>')