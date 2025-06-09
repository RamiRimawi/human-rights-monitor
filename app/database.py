from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["human_rights_monitor"]

case_collection = db["cases"]
