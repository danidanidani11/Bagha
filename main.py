import telebot, json, os, datetime, random
from flask import Flask, request
from telebot import types
from threading import Thread

API_TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
bot = telebot.TeleBot(API_TOKEN)
bot.set_my_commands([
    telebot.types.BotCommand("start", "شروع ربات"),
])
CHANNEL_USERNAME = "@bagha_game"
ADMIN_ID = 5542927340
TRON_ADDRESS = "TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb"

app = Flask(__name__)

DATA_FILE = "users.json"
QUESTIONS_FILE = "questions.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(QUESTIONS_FILE):
    sample_questions = [
        {
            "question": "✈️ [مرحله 1] هواپیما سقوط کرده و شما در جنگلی تاریک هستید. اولین واکنش شما چیست؟",
            "options": ["🏃 فرار می‌کنم", "🧭 نقشه می‌کشم", "🔥 آتش روشن می‌کنم", "😱 تسلیم می‌شوم"],
            "answer": 2,
            "explanations": {
                0: "فرار بدون هدف ممکن است باعث گم‌شدگی بیشتر شود.",
                1: "نقشه کشیدن بدون دید کافی بی‌فایده است.",
                2: "✅ روشن کردن آتش باعث دیده شدن توسط تیم نجات می‌شود.",
                3: "تسلیم شدن به معنای پایان تلاش برای بقا است."
            }
        },
        {
            "question": "🌲 [مرحله 2] صدای شکست شاخه‌ای در پشت سرت می‌شنوی. چه می‌کنی؟",
            "options": ["🔁 برمی‌گردم", "🏃 سریع دور می‌شوم", "🙈 پنهان می‌شوم", "📣 فریاد می‌زنم"],
            "answer": 2,
            "explanations": {
                0: "برگشتن می‌تواند باعث رویارویی ناگهانی با خطر شود.",
                1: "فرار صدای بیشتری تولید می‌کند.",
                2: "✅ پنهان شدن در سکوت بهترین انتخاب برای حفظ جان است.",
                3: "فریاد زدن خطر را به سمت شما می‌کشاند."
            }
        }
    ]
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(sample_questions, f)

with open(QUESTIONS_FILE) as f:
    QUESTIONS = json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def load_users():
    with open(DATA_FILE) as f:
        return json.load(f)

def is_member(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'creator', 'administrator']
    except:
        return False

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 شروع بازی", "🏆 برترین ها")
    markup.add("🛒 فروشگاه", "🧑‍🤝‍🧑 دعوت دوستان")
    markup.add("👤 پروفایل", "🎁 پاداش روزانه")
    return markup

@bot.message_handler(commands=['start'])
def handle_start(m):
    user_id = str(m.chat.id)
    users = load_users()
    
    if not is_member(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
        bot.send_message(user_id, "📛 برای استفاده از ربات، ابتدا باید در کانال عضو شوید:", reply_markup=markup)
        return
    
    if user_id not in users:
        users[user_id] = {
            "name": "",
            "life": 3,
            "coin": 0,
            "score": 0,
            "step": 0,
            "last_bonus": ""
        }
        save_users(users)
    
    if not users[user_id]["name"]:
        msg = bot.send_message(user_id, "👤 لطفاً نام واقعی خود را وارد کنید (حداقل 2 حرف):", 
                             reply_markup=types.ForceReply(selective=True))
        bot.register_next_step_handler(msg, process_name)
    else:
        bot.send_message(user_id, f"🔹 سلام {users[user_id]['name']}!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.reply_to_message and "نام خود را وارد کن" in m.reply_to_message.text)
def process_name(m):
    text = m.text.strip()
    if len(text) < 2:
        bot.send_message(m.chat.id, "❗️نام باید حداقل 2 حرف باشد. لطفاً مجدداً وارد کنید:")
        return

    users = load_users()
    users[str(m.chat.id)]["name"] = text
    save_users(users)
    bot.send_message(m.chat.id, f"✅ ثبت شد: {text}", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🎮 شروع بازی")
def start_game(m):
    users = load_users()
    user_id = str(m.chat.id)
    
    if user_id not in users:
        bot.send_message(m.chat.id, "❌ کاربر یافت نشد. لطفاً /start را بزنید.")
        return
        
    user = users[user_id]
    
    if user["life"] <= 0:
        bot.send_message(m.chat.id, "❌ شما جان ندارید! لطفاً از فروشگاه جان بخرید.")
        return
        
    if user["step"] >= len(QUESTIONS):
        bot.send_message(m.chat.id, "🎉 شما تمام مراحل را گذرانده‌اید!")
        return
        
    send_question(m.chat.id)

def is_valid_answer(m):
    users = load_users()
    user_id = str(m.chat.id)
    
    if user_id not in users:
        return False
        
    user = users[user_id]
    step = user.get("step", 0)
    
    if step >= len(QUESTIONS):
        return False
    
    q = QUESTIONS[step]
    return any(m.text.strip() == opt.strip() for opt in q["options"])

@bot.message_handler(func=is_valid_answer)
def answer_question(m):
    users = load_users()
    user_id = str(m.chat.id)
    user = users[user_id]
    step = user["step"]

    q = QUESTIONS[step]
    options = q["options"]
    explanations = q["explanations"]
    correct_index = q["answer"]

    selected_index = options.index(m.text.strip())

    if selected_index == correct_index:
        user["coin"] += 10
        user["score"] += 20
        result = f"✅ درست گفتی!\n📘 توضیح: {explanations[selected_index]}"
    else:
        user["score"] += 5
        result = f"❌ اشتباه بود!\n📘 توضیح: {explanations[selected_index]}"

    all_expl = "\n\n📖 توضیح تمام گزینه‌ها:\n"
    for i, opt in enumerate(options):
        mark = "✅" if i == correct_index else "❌"
        all_expl += f"{mark} {opt}: {explanations[i]}\n"

    bot.send_message(m.chat.id, result + all_expl)

    user["step"] += 1
    save_users(users)

    if user["step"] < len(QUESTIONS):
        send_question(m.chat.id)
    else:
        bot.send_message(m.chat.id, "🏁 تمام مراحل به پایان رسید!", reply_markup=main_menu())

def send_question(chat_id):
    users = load_users()
    user_id = str(chat_id)
    
    if user_id not in users:
        return
        
    user = users[user_id]
    step = user["step"]
    
    if step < len(QUESTIONS):
        q = QUESTIONS[step]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        
        for opt in q["options"]:
            markup.add(opt)
            
        markup.add("🔙 بازگشت به منو")
        bot.send_message(chat_id, q["question"], reply_markup=markup)
    else:
        bot.send_message(chat_id, "🎉 شما همه مراحل را کامل کردید!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به منو")
def back_to_menu(m):
    bot.send_message(m.chat.id, "↩️ بازگشت به منو", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 فروشگاه")
def shop(m):
    msg = f"""🛒 فروشگاه:

💰 قیمت ۱۰۰ سکه = ۴ ترون  
💳 آدرس ترون: `{TRON_ADDRESS}`

✅ پس از پرداخت، همین پیام را ریپلای و فیش را ارسال کنید (عکس یا متن).

📍 همچنین می‌توانید با ۱۰۰ سکه، ۱ ❤️ جان بخرید:
برای خرید جان، گزینه زیر را انتخاب کنید:
"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🧡 خرید جان (۱۰۰ سکه)", "🔙 بازگشت به منو")
    bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🧡 خرید جان (۱۰۰ سکه)")
def buy_life(m):
    users = load_users()
    u = users[str(m.chat.id)]
    if u["coin"] >= 100:
        u["coin"] -= 100
        u["life"] += 1
        save_users(users)
        bot.send_message(m.chat.id, "🧡 یک جان با موفقیت خریداری شد! ❤️")
    else:
        bot.send_message(m.chat.id, "❌ شما سکه کافی برای خرید جان ندارید.")

@bot.message_handler(func=lambda m: m.text == "👤 پروفایل")
def profile(m):
    users = load_users()
    u = users[str(m.chat.id)]
    msg = f"""👤 نام: {u['name']}
❤️ جان: {u['life']}
💰 سکه: {u['coin']}
⭐️ امتیاز: {u['score']}"""
    bot.send_message(m.chat.id, msg)

@bot.message_handler(func=lambda m: m.text == "🎁 پاداش روزانه")
def daily_bonus(m):
    users = load_users()
    user_id = str(m.chat.id)
    
    if user_id not in users:
        bot.send_message(m.chat.id, "❌ خطا در یافتن اطلاعات کاربر. لطفاً با /start مجدداً شروع کنید.")
        return
    
    user = users[user_id]
    now = datetime.datetime.now()
    
    if "last_bonus" not in user or not user["last_bonus"]:
        user["last_bonus"] = "2000-01-01 00:00:00"
    
    try:
        last = datetime.datetime.strptime(user["last_bonus"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        last = datetime.datetime.min
        user["last_bonus"] = "2000-01-01 00:00:00"
    
    delta = now - last
    
    if delta.total_seconds() >= 43200:
        user["coin"] += 10
        user["last_bonus"] = now.strftime("%Y-%m-%d %H:%M:%S")
        save_users(users)
        bot.send_message(m.chat.id, "🎉 ۱۰ سکه پاداش دریافت کردید!")
    else:
        remaining = 43200 - delta.total_seconds()
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        bot.send_message(m.chat.id, f"⏳ باید {hours} ساعت و {minutes} دقیقه دیگر صبر کنید.")

@bot.message_handler(func=lambda m: m.text == "🧑‍🤝‍🧑 دعوت دوستان")
def invite(m):
    link = f"https://t.me/{bot.get_me().username}?start={m.chat.id}"
    bot.send_message(m.chat.id, f"📨 لینک دعوت شما:\n{link}\nهر دعوت = ۵۰ سکه")

@bot.message_handler(func=lambda m: m.text == "🏆 برترین ها")
def top_players(m):
    users = load_users()
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
    text = "🏆 ۱۰ بازیکن برتر:\n"
    for i, (uid, u) in enumerate(sorted_users[:10]):
        text += f"{i+1}. {u['name']} - {u['score']} امتیاز\n"
    bot.send_message(m.chat.id, text)

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "بات فعال است"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://bagha-2qv0.onrender.com/{API_TOKEN}")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    if m.text and m.text.startswith('/start'):
        return
        
    users = load_users()
    user_id = str(m.chat.id)
    
    if user_id not in users or not users[user_id].get("name"):
        bot.send_message(m.chat.id, "❗️ لطفاً ابتدا با دستور /start ثبت نام کنید.")
        return
        
    if is_valid_answer(m):
        return
        
    bot.send_message(m.chat.id, "⚠️ لطفاً از منوی اصلی انتخاب کنید.", reply_markup=main_menu())

if __name__ == "__main__":
    Thread(target=run).start()
