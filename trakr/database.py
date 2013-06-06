from pymongo import MongoClient
from bson import ObjectId

client = None
db = None

def connect(host='127.0.0.1', port=27017):
    client = MongoClient(host, port)
    db = client.trakr
    
    return db

db = connect()
