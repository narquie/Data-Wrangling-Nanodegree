## Amount of unique contributors
from pymongo import MongoClient
def get_node(db):
    return len(db.OSMLagny.distinct("created.user"))
def get_db():
    client = MongoClient('localhost:27017')
    db = client.mongData
    return db

if __name__ == "__main__":
    db = get_db()
    print get_node(db)