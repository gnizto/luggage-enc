import os
import json
import csv
import hashlib
import random
import string
import argparse
from datetime import datetime

DB_PATH = "../site/data.json"
CSV_PATH = "../site/data.csv"

# -----------------------------
# ID GENERATOR (alphanumeric)
# Pattern: XXX-XXXX (letters+numbers)
# -----------------------------
def generate_id():
    def block(n):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(n))
    return f"{block(3)}-{block(4)}"

# -----------------------------
# PASSPHRASE GENERATOR
# readable + strong enough
# -----------------------------
WORDS = [
    "Stone", "River", "Cloud", "Night", "Wind",
    "Forest", "Anchor", "Sky", "Lion", "Echo",
    "Bark", "Wave", "Star", "Flame", "Path"
]

def generate_passphrase():
    return "-".join([
        random.choice(WORDS),
        random.choice(WORDS),
        random.choice(WORDS),
        str(random.randint(10, 99))
    ])

# -----------------------------
# HASH
# -----------------------------
def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

# -----------------------------
# LOAD/SAVE JSON
# -----------------------------
def load_json():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return {"meta": {}, "items": {}}

def save_json(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

# -----------------------------
# CSV WRITER
# -----------------------------
def save_csv(db, item_id: str, passphrase: str):
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH):
            writer.writerow([
                "id", "name", "passphrase", "passphrase_hash", "created_at"
            ])
        
        writer.writerow([
                item_id,
                db["items"][item_id]["name"],
                passphrase,
                db["items"][item_id]["challenge"]["hash"],
                db["items"][item_id]["created_at"]
            ])

        # writer.writerow([
        #     "id", "name", "passphrase", "passphrase_hash", "created_at"
        # ])

        # for k, v in db["items"].items():
        #     writer.writerow([
        #         k,
        #         v["name"],
        #         passphrase
        #         v["challenge"]["hash"],
        #         v["created_at"]
        #     ])

# -----------------------------
# ADD ITEM
# -----------------------------
def add_item(args):
    db = load_json()

    item_id = generate_id()
    passphrase = generate_passphrase()

    db["items"][item_id] = {
        "name": args.name,
        "created_at": datetime.utcnow().isoformat(),
        "challenge": {
            "hash": sha256(passphrase)
        }
    }

    save_json(db)
    save_csv(db, item_id, passphrase)

    print("\n✔ ITEM CREATED")
    print("ID:", item_id)
    print("PASSPHRASE:", passphrase)
    print("\n(Keep passphrase safe — it is not stored in plain text)\n")

# -----------------------------
# LIST ITEMS
# -----------------------------
def list_items():
    db = load_json()
    for k, v in db["items"].items():
        print(k, "->", v["name"])

# -----------------------------
# CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers()

    add = sub.add_parser("add")
    add.add_argument("--name", required=True)
    add.set_defaults(func=add_item)

    ls = sub.add_parser("list")
    ls.set_defaults(func=lambda _: list_items())

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()