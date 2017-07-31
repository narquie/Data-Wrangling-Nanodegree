import xml.etree.cElementTree as ET
import pprint

## Adds count of tags across OSM XML
def count_tags(filename):
    dict = {}
    ## Iterates over all tags
    for event, elem in ET.iterparse(filename):
        if elem.tag not in dict:
            dict[elem.tag] = 1
        else:
            dict[elem.tag] += 1
    return(dict)

def query():
    tags = count_tags('OSM Lagny')
    pprint.pprint(tags)

if __name__ == "__main__":
    query()