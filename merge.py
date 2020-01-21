#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:13:02 2019

@author: sebastianw
"""

import argparse
import csv
import json
import xmltodict

class HashableDict(dict):
    def __hash__(self):
        return hash(json.dumps(self, sort_keys=True))

def read_data(*files):
    data = set()
    for file in files:
        for element in xmltodict.parse(file.read())['gpx']['wpt']:
            data.add(HashableDict(element))

    data = sorted(data, key=lambda x: float(x['@lat']) + float(x['@lon']))

    categories = {}
    for wpt in data:
        if 'extensions' not in wpt:
            continue
        categories[wpt['type']] = wpt['extensions']['color']
        del wpt['extensions']

    return data, categories


def write_csv(data, categories, csvfile, categoriesfile):
    fieldnames = ['@lat', '@lon', 'name', 'cmt', 'desc', 'type']
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    writer.writerows(data)
    json.dump(categories, categoriesfile,
              sort_keys=True, indent=True)

def read_csv(handle):
    return list(csv.DictReader(handle))

def write_gpx(data, colors, handle):
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

def gpx2csv(args):
    data, categories = read_data(*args.gpxfiles)
    write_csv(data, categories, args.outfile, args.categories)


def csv2gpx(args):
    data = read_csv(args.infile)
    categories = json.load(args.categories)
    write_gpx(data, categories, args.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('gpx-favourites-merge')
    subparsers = parser.add_subparsers()
    gpx2csvp = subparsers.add_parser('gpx2csv')
    gpx2csvp.add_argument('gpxfiles', nargs="+", type=argparse.FileType('r'))
    gpx2csvp.add_argument('outfile', type=argparse.FileType('w'))
    gpx2csvp.add_argument('categories', type=argparse.FileType('w'))
    gpx2csvp.set_defaults(func=gpx2csv)
    csv2gpxp = subparsers.add_parser('csv2gpx')
    csv2gpxp.add_argument('infile', type=argparse.FileType('r'))
    csv2gpxp.add_argument('categories', type=argparse.FileType('r'))
    csv2gpxp.add_argument('outfile', type=argparse.FileType('w'))
    csv2gpxp.set_defaults(func=csv2gpx)
    args = parser.parse_args()
    args.func(args)
