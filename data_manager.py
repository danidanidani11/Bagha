import json
import os

DATA_FILE = "users.json"

# اگه فایل وجود داره، لودش کن؛ وگرنه فایل خالی بساز
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = {}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_user(user_id):
    return users.get(str(user_id), None)

def save_user(user_id, user_data):
    users[str(user_id)] = user_data
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
