# services/storage_handler.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["leadscoring"]

# Offers
def save_offer(offer):
    db.offers.delete_many({})  # keep only one active offer
    db.offers.insert_one(offer)

def load_offer():
    return db.offers.find_one({}, {"_id": 0})

# Leads
def save_leads(leads):
    db.leads.delete_many({})
    db.leads.insert_many(leads)

def load_leads():
    return list(db.leads.find({}, {"_id": 0}))

# Results
def save_results(results):
    db.results.delete_many({})
    db.results.insert_many(results)

def load_results():
    return list(db.results.find({}, {"_id": 0}))

