import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import json
OSMFILE = "OSM Lagny"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Rue"]

## French language specific updates
mapping = { "rue": "Rue",
            "place": "Place",
            "av.": "Avenue",
            "avenue": "Avenue",
            "cours": "Cours"
            }

## Adds streets not in expected to a dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

## Identifies if the tag is a street
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


## Iterates through the XML finding street names
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

## Updates names based on the French names in -mapping-
def update_name(name, mapping):
    for i in mapping.keys():
        if i in name:
            name = name.replace(i,mapping[i])
            break
    return name

## Shows a few sample names 
def query():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

if __name__ == '__main__':
    query()