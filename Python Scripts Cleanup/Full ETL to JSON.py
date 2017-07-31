import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import json
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

## Udacity-advised fields to put into a sub-category
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

mapping = { "rue": "Rue",
            "place": "Place",
            "av.": "Avenue",
            "avenue": "Avenue",
            "cours": "Cours"
            }
## Used to identify keys that are street names
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

## Updates based on -mapping-
def update_name(name, mapping):
    for i in mapping.keys():
        if i in name:
            name = name.replace(i,mapping[i])
            break
    return name

## Changes the keys and values to fit a very specific JSON format for MongoDB use
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag
        node["created"] = {}
        ## Specific list "node_refs" for "way" tag only
        if element.tag == "way":
            node["node_refs"] = []
        for tag in element.iter():
            for tagged in tag.attrib:
                if tagged == "k":
                    if ":" not in tag.attrib["k"]:
                        node[tag.attrib["k"]] =  tag.attrib["v"]
                    elif len(tag.attrib["k"].split(":"))<3 and not problemchars.search(tagged):
                        ## Cleans up street names for end use i.e. av. => Avenue
                        if is_street_name(tag):
                            for name in tag.attrib['v']:
                                better_name = update_name(name, mapping)
                                newKey = tag.attrib["k"].split(":")[1]
                                if tag.attrib["k"].split(":")[0] == "addr":
                                    tempKey = "address"
                                else:
                                    tempKey = tag.attrib["k"].split(":")[0]
                                ## Temporary dictionary to be fitted as sub-category in JSON
                                tempDict = {newKey:better_name}
                                if tempKey in node and type(node[tempKey]) == dict:
                                    node[tempKey][newKey] = better_name
                                else:
                                    node[tempKey] = tempDict
                        ## If not a street name, process as usual
                        else:
                            newKey = tag.attrib["k"].split(":")[1]
                            if tag.attrib["k"].split(":")[0] == "addr":
                                tempKey = "address"
                            else:
                                tempKey = tag.attrib["k"].split(":")[0]
                            ## Temporary dictionary to be fitted as sub-category in JSON
                            tempDict = {newKey:tag.attrib["v"]}
                            if tempKey in node and type(node[tempKey]) == dict:
                                node[tempKey][newKey] = tag.attrib["v"]
                            else:
                                node[tempKey] = tempDict
                ## Checks for all tags that go into the created sub dict
                elif tagged in CREATED:
                    node["created"][tagged] = tag.attrib[tagged]
                ## Checks for lat and puts it into sub list -pos-
                elif tagged == "lat":
                    if 'pos' in node:
                        node["pos"][0] = float(tag.attrib[tagged])
                    else:
                        node["pos"] = [float(tag.attrib[tagged]),0]
                ## Checks for lon and puts it into sub list -pos-
                elif tagged == "lon":
                    if 'pos' in node:
                        node["pos"][1] = float(tag.attrib[tagged])
                    else:
                        node["pos"] = [0,float(tag.attrib[tagged])]
                ## Checks for ref and puts it into sub list -ref-
                elif tagged == "ref":
                    node["node_refs"].append(tag.attrib[tagged])
                ## Catches all other tags    
                elif tagged != "v":
                    node[tagged] = tag.attrib[tagged]
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    ## Ports the dictionary created to a JSON file
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def execute():
    data = process_map('OSM Lagny', False)

if __name__ == "__main__":
    execute()