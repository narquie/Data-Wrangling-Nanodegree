import xml.etree.cElementTree as ET
import pprint
import re

## Regular expressions used to find problematic / anomalistic keys

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

## Returns key counts based on different sections (i.e. lower, lower_colon, problemchars, other)
def key_type(element, keys):
    otherKey = []
    if element.tag == "tag":
        ## Uses regular expressions above to search over keys
        for tag in element.iter("tag"):
            if re.search(lower,tag.attrib['k']) is not None:
                keys["lower"] += 1
            elif re.search(lower_colon,tag.attrib['k']) is not None:
                keys["lower_colon"] += 1
            elif re.search(problemchars,tag.attrib['k']) is not None:
                keys["problemchars"] += 1
            else:
                keys["other"] += 1
                ## Pulls the specific names of keys that are "other" for further analysis
                otherKey.append(tag.attrib['k'])
    if len(otherKey)>0:
        return keys,otherKey
    else:
        return keys, None
    
## Takes in the "other" keys as output, and receives the key dictionary as a whole
def process_map(filename):
    other = ""
    otherList = []
    otherDict = {}
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys,other = key_type(element, keys)
        if other != None:
            otherList.append(other)
    for i in otherList:
        if i[0] in otherDict:
            otherDict[i[0]] += 1
        else:
            otherDict[i[0]] = 1
    pprint.pprint(otherDict)
    return keys



def query():
    keys = process_map('OSM Lagny')
    pprint.pprint(keys)


if __name__ == "__main__":
    query()