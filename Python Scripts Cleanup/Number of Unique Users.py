import xml.etree.cElementTree as ET
import pprint
import re

## Creates a unique set of users for review
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        for tag in element.iter():
            if "uid" in tag.attrib:
                if tag.attrib["uid"] not in users:
                    users.add(tag.attrib["uid"])
    return users


def query():

    users = process_map('OSM Lagny')
    pprint.pprint(users)
    pprint.pprint(len(users))

if __name__ == "__main__":
    query()