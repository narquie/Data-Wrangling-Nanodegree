## Amount of amenities
from pymongo import MongoClient
def get_node(db):
    return list(db.OSMLagny.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity",
"count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]))
def get_db():
    client = MongoClient('localhost:27017')
    db = client.mongData
    return db

if __name__ == "__main__":
    db = get_db()
    pprint.pprint(get_node(db))