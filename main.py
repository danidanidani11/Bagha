import telebot, json, os, datetime, random
from flask import Flask, request
from telebot import types
from threading import Thread

API_TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
CHANNEL_USERNAME = "@bagha_game"
ADMIN_ID = 5542927340
TRON_ADDRESS = "TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

DATA_FILE = "users.json"
QUESTIONS_FILE = "questions.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# ✅ بارگذاری سوالات از فایل یا ساخت اولیه
if not os.path.exists(QUESTIONS_FILE):
    sample_questions = []
    for i in range(30):
        sample_questions.append({
            "question": f"✈️ [مرحله {i+1}] شما پس از سقوط هواپیما در یک منطقه ترسناک با موقعیتی بحرانی مواجه می‌شوید...\nچه کار می‌کنید؟",
            "options": ["🏃 فرار می‌کنم", "🧭 نقشه می‌کشم", "🔥 آتش روشن می‌کنم", "😱 تسلیم می‌شوم"],
            "answer": 2,
            "explanation": "روشن کردن آتش باعث دیده شدن شما توسط نجات‌دهنده‌ها می‌شود."
        })
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

def check_membership(user_id):
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
def start(m):
    users = load_users()

    # ✅ عضویت اجباری در کانال
    if not check_membership(m.chat.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(btn)
        bot.send_message(m.chat.id, "🔒 برای استفاده از ربات، ابتدا در کانال زیر عضو شوید و سپس دوباره /start را بفرستید:", reply_markup=markup)
        return

    # ✅ ثبت کاربر و گرفتن اسم
    if str(m.chat.id) not in users:
        users[str(m.chat.id)] = {
            "name": "",
            "coin": 0,
            "life": 3,
            "score": 0,
            "step": 0,
            "last_bonus": "0",
            "ref": 0
        }
        save_users(users)
        bot.send_message(m.chat.id, "👋 سلام! لطفاً نام خود را وارد کنید:")
        bot.register_next_step_handler(m, get_name)
    else:
        bot.send_message(m.chat.id, "👋 خوش آمدید!", reply_markup=main_menu())
def get_name(m):
    users = load_users()
    users[str(m.chat.id)]["name"] = m.text
    save_users(users)
    bot.send_message(m.chat.id, f"✅ به بازی بقا خوش آمدی {m.text}!", reply_markup=main_menu())

# 🎮 بازی
@bot.message_handler(func=lambda m: m.text == "🎮 شروع بازی")
def start_game(m):
    users = load_users()
    u = users[str(m.chat.id)]
    if u["life"] <= 0:
        bot.send_message(m.chat.id, "❌ شما جان ندارید! لطفاً از فروشگاه جان بخرید.")
        return
    if u["step"] >= len(QUESTIONS):
        bot.send_message(m.chat.id, "🎉 شما تمام مراحل را گذرانده‌اید!")
        return
    q = QUESTIONS[u["step"]]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i, opt in enumerate(q["options"]):
        markup.add(f"{i+1} - {opt}")
    markup.add("🔙 بازگشت به منو")
    bot.send_message(m.chat.id, q["question"], reply_markup=markup)

@bot.message_handler(func=lambda m: m.text.startswith(tuple(str(i+1) for i in range(4))))
def answer_question(m):
    users = load_users()
    u = users[str(m.chat.id)]
    if u["step"] >= len(QUESTIONS):
        return
    q = QUESTIONS[u["step"]]
    selected = int(m.text.split("-")[0].strip()) - 1
    if selected == q["answer"]:
        u["coin"] += 10
        u["score"] += 20
        bot.send_message(m.chat.id, "✅ درست بود! ۱۰ سکه و ۲۰ امتیاز گرفتی.")
    else:
        u["score"] += 5
        bot.send_message(m.chat.id, f"❌ اشتباه بود. دلیل: {q['explanation']}")
    u["step"] += 1
    save_users(users)
    start_game(m)

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به منو")
def back_to_menu(m):
    bot.send_message(m.chat.id, "↩️ بازگشت به منو", reply_markup=main_menu())

# 🛒 فروشگاه - منو
@bot.message_handler(func=lambda m: m.text == "🛒 فروشگاه")
def shop(m):
    msg = f"""🛒 فروشگاه:

💰 قیمت ۱۰۰ سکه = ۴ ترون  
💳 آدرس ترون: `{TRON_ADDRESS}`

✅ پس از پرداخت، فیش را ارسال کنید (عکس یا متن).

📍 همچنین می‌توانید با ۱۰۰ سکه، ۱ ❤️ جان بخرید:
برای خرید جان، گزینه زیر را انتخاب کنید:
"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🧡 خرید جان (۱۰۰ سکه)", "🔙 بازگشت به منو")
    markup.add("💳 ارسال فیش پرداخت")
    bot.send_message(m.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

# ❤️ خرید جان با ۱۰۰ سکه
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

# 💳 ارسال فیش پرداخت (درخواست)
@bot.message_handler(func=lambda m: m.text == "💳 ارسال فیش پرداخت")
def ask_payment(m):
    bot.send_message(m.chat.id, "📸 لطفاً فیش پرداخت را به صورت *عکس* یا *متن* ارسال کن:", reply_markup=types.ForceReply(), parse_mode="Markdown")

# 📤 دریافت فیش پرداخت و ارسال برای ادمین
@bot.message_handler(func=lambda m: m.reply_to_message and "فیش" in m.reply_to_message.text)
def handle_payment(m):
    msg = f"📥 فیش پرداخت جدید از {m.from_user.first_name}:\n\n"
    if m.content_type == "photo":
        file_id = m.photo[-1].file_id
        bot.send_photo(ADMIN_ID, file_id, caption=msg + "(فیش تصویری)", reply_markup=payment_markup(m.chat.id))
    else:
        bot.send_message(ADMIN_ID, msg + m.text, reply_markup=payment_markup(m.chat.id))

# ✅ دکمه‌های تایید / رد برای ادمین
def payment_markup(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ تایید", callback_data=f"approve_{user_id}"))
    markup.add(types.InlineKeyboardButton("❌ رد", callback_data=f"reject_{user_id}"))
    return markup

# ✅ تایید پرداخت توسط ادمین
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_payment(call):
    user_id = call.data.split("_")[1]
    users = load_users()
    users[user_id]["coin"] += 100
    save_users(users)
    bot.send_message(int(user_id), "✅ پرداخت شما تایید شد! ۱۰۰ سکه به حساب شما اضافه شد.")
    bot.answer_callback_query(call.id, "پرداخت تایید شد.")

# ❌ رد پرداخت توسط ادمین با پیام دقیق‌تر
@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_payment(call):
    user_id = call.data.split("_")[1]
    bot.send_message(int(user_id), "❌ رسید پرداخت شما توسط ادمین رد شد.\nلطفاً بررسی و در صورت نیاز، مجدداً ارسال کنید.")
    bot.answer_callback_query(call.id, "رد شد.")

# 👤 پروفایل
@bot.message_handler(func=lambda m: m.text == "👤 پروفایل")
def profile(m):
    users = load_users()
    u = users[str(m.chat.id)]
    msg = f"""👤 نام: {u['name']}
❤️ جان: {u['life']}
💰 سکه: {u['coin']}
⭐️ امتیاز: {u['score']}"""
    bot.send_message(m.chat.id, msg)

# 🎁 پاداش روزانه
@bot.message_handler(func=lambda m: m.text == "🎁 پاداش روزانه")
def daily_bonus(m):
    users = load_users()
    u = users[str(m.chat.id)]
    last = datetime.datetime.strptime(u["last_bonus"], "%Y-%m-%d") if u["last_bonus"] != "0" else datetime.datetime.min
    now = datetime.datetime.now()
    if (now - last).days >= 1:
        u["coin"] += 10
        u["last_bonus"] = now.strftime("%Y-%m-%d")
        save_users(users)
        bot.send_message(m.chat.id, "🎉 ۱۰ سکه پاداش گرفتی!")
    else:
        bot.send_message(m.chat.id, "⏳ پاداش روزانه‌ات رو قبلا گرفتی. فردا بیا!")

# 🧑‍🤝‍🧑 دعوت
@bot.message_handler(func=lambda m: m.text == "🧑‍🤝‍🧑 دعوت دوستان")
def invite(m):
    link = f"https://t.me/{bot.get_me().username}?start={m.chat.id}"
    bot.send_message(m.chat.id, f"📨 لینک دعوت شما:\n{link}\nهر دعوت = ۵۰ سکه")

# 🎖️ برترین‌ها
@bot.message_handler(func=lambda m: m.text == "🏆 برترین ها")
def top_players(m):
    users = load_users()
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
    text = "🏆 ۱۰ بازیکن برتر:\n"
    for i, (uid, u) in enumerate(sorted_users[:10]):
        text += f"{i+1}. {u['name']} - {u['score']} امتیاز\n"
    bot.send_message(m.chat.id, text)

# 🌐 Flask برای دیپلوی در Render
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
    bot.set_webhook(url=f"https://bagha-2qv0.onrender.com/{API_TOKEN}")  # 🔁 آدرس دقیق Render

if __name__ == "__main__":
    Thread(target=run).start()
