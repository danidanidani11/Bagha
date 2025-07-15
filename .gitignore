import json

# ذخیره داده‌ها در فایل
def save_data(user_id, data):
    try:
        with open("user_data.json", "r") as f:
            all_data = json.load(f)
    except FileNotFoundError:
        all_data = {}
    
    all_data[user_id] = data  # اضافه کردن داده جدید
    
    with open("user_data.json", "w") as f:
        json.dump(all_data, f)  # ذخیره کل داده‌ها

# خواندن داده‌ها
def get_data(user_id):
    try:
        with open("user_data.json", "r") as f:
            all_data = json.load(f)
            return all_data.get(user_id)
    except FileNotFoundError:
        return None
