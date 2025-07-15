import sqlite3
import os
from pathlib import Path

# مسیر دائمی برای دیتابیس (حتی پس از Deploy)
DB_PATH = Path(__file__).parent / "bagha_db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id TEXT PRIMARY KEY, 
                       data TEXT)''')
    conn.commit()
    conn.close()

def save_user(user_id, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", 
                  (str(user_id), str(data)))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM users WHERE user_id=?", (str(user_id),))
    result = cursor.fetchone()
    conn.close()
    return eval(result[0]) if result else None
