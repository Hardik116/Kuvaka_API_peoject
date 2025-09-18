import json
import pandas as pd
import os

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

def save_offer(offer):
    with open(os.path.join(STORAGE_DIR, "offer.json"), "w") as f:
        json.dump(offer, f)

def load_offer():
    path = os.path.join(STORAGE_DIR, "offer.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_leads(leads):
    df = pd.DataFrame(leads)
    df.to_csv(os.path.join(STORAGE_DIR, "leads.csv"), index=False)

def load_leads():
    path = os.path.join(STORAGE_DIR, "leads.csv")
    if os.path.exists(path):
        return pd.read_csv(path).to_dict(orient="records")
    return []

def save_results(results):
    with open(os.path.join(STORAGE_DIR, "results.json"), "w") as f:
        json.dump(results, f)

def load_results():
    path = os.path.join(STORAGE_DIR, "results.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []
