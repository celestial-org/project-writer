from lib.env import mongo_url
from pymongo import MongoClient

mongo = MongoClient(mongo_url)
v2ray_notes = mongo["notes"]
savessh = mongo["ssh"]

