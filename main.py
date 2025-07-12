import os, json, time, threading
from flask import Flask, request
import telebot
from telebot import types

API_TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
CHANNEL_USERNAME = "@bagha_game"
ADMIN_ID = 5542927340
TRON_ADDRESS = "TJ4xrwKzKjk6FgKfuuqwah3Az5Ur22kJb"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
data_file = "users.json"
questions_file = "questions.json"

if not os.path.exists(data_file):
    with open(data_file, "w") as f:
        json.dump({}, f)

if not os.path.exists(questions_file):
    questions = []
    for i in range(1, 51):
        questions.append({
            "question": f"✈️ مرحله {i} - هواپیمای تو سقوط کرده. تو جنگل بیدار شدی... اولین واکنش تو؟",
            "options": [
                {"text": "بررسی اطراف برای غذا", "correct": i % 2 == 1, "reason": "در مراحل اولیه بقا، غذا مهم‌ترینه."},
                {"text": "تلاش برای تماس اضطراری", "correct": i % 5 == 0, "reason": "اگر دستگاه ارتباطی کار کنه بهترین کاره."},
                {"text": "پنهان شدن تا شب", "correct": i % 3 == 0, "reason": "ممکنه خطرناک باشه چون دید کم میشه."},
                {"text": "رفتن به دل جنگل", "correct": False, "reason": "بدون تجهیزات گم میشی یا با حیوانات روبرو میشی."}
            ]
        })
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False)

def load_data():
    with open(data_file) as f:
        return json.load(f)

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f)

def check_membership(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

def get_main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎮 شروع بازی", "🏆 برترین‌ها")
    kb.row("🛒 فروشگاه", "👥 دعوت دوستان")
    kb.row("👤 پروفایل", "🎁 پاداش روزانه")
    return kb

def get_confirm_membership_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("✅ تایید عضویت در کانال")
    return kb

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    data = load_data()

    if not check_membership(message.chat.id):
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        bot.send_message(message.chat.id, "🔒 برای استفاده از ربات، ابتدا عضو کانال شو.", reply_markup=join_btn)
        return

    # اگر عضو کانال ولی تایید نکرده
    if user_id in data and data[user_id].get("membership_confirmed") != True:
        bot.send_message(message.chat.id, "لطفاً عضویت در کانال را با زدن دکمه زیر تأیید کن.", reply_markup=get_confirm_membership_menu())
        return

    # ثبت‌نام
    if user_id not in data:
        bot.send_message(message.chat.id, "👋 خوش اومدی! لطفا اسم بازیکنتو بنویس:")
        data[user_id] = {"step": "get_name", "membership_confirmed": True}
        save_data(data)
        return

    bot.send_message(message.chat.id, f"سلام {data[user_id]['name']} 👋", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = str(message.chat.id)
    data = load_data()
    user = data.get(user_id)

    if not user:
        bot.send_message(message.chat.id, "اول /start رو بزن.")
        return

    # تایید عضویت کانال
    if message.text == "✅ تایید عضویت در کانال":
        if check_membership(message.chat.id):
            user["membership_confirmed"] = True
            save_data(data)
            bot.send_message(message.chat.id, "✅ عضویت شما تأیید شد. حالا لطفا اسم بازیکنتو بنویس:")
            user["step"] = "get_name"
            save_data(data)
        else:
            join_btn = types.InlineKeyboardMarkup()
            join_btn.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
            bot.send_message(message.chat.id, "❌ هنوز عضو کانال نیستی! لطفا اول عضو شو.", reply_markup=join_btn)
        return

    if user.get("step") == "get_name":
        name = message.text.strip()
        user.update({
            "name": name,
            "coins": 0,
            "hearts": 3,    # شروع با 3 جون
            "score": 0,
            "last_reward": 0,
            "step": None,
            "current_q": 0,
            "membership_confirmed": True
        })
        save_data(data)
        bot.send_message(message.chat.id, f"✅ نام ثبت شد: {name}", reply_markup=get_main_menu())
        return

    # پاسخ به سوال
    if user.get("step") == "answering":
        with open(questions_file, "r", encoding="utf-8") as f:
            questions = json.load(f)

        q = questions[user["current_q"]]
        answer = message.text.strip()

        if answer == "🔙 بازگشت به منو":
            user["step"] = None
            save_data(data)
            bot.send_message(message.chat.id, "منو اصلی 👇", reply_markup=get_main_menu())
            return

        correct = next((opt for opt in q["options"] if opt["text"] == answer and opt["correct"]), None)

        if correct:
            bot.send_message(message.chat.id, "✅ جواب درست! +10 سکه، +20 امتیاز")
            user["coins"] += 10
            user["score"] += 20
        else:
            reason = next((opt["reason"] for opt in q["options"] if opt["text"] == answer), "نامشخص.")
            bot.send_message(message.chat.id, f"❌ اشتباه! دلیل: {reason}\n+5 امتیاز، -1 جان")
            user["score"] += 5
            user["hearts"] -= 1
            if user["hearts"] <= 0:
                bot.send_message(message.chat.id, "💀 تو باختی. جانت تموم شد.", reply_markup=get_main_menu())
                user["step"] = None
                save_data(data)
                return

        user["current_q"] += 1
        user["step"] = None
        save_data(data)

        if user["current_q"] >= len(questions):
            bot.send_message(message.chat.id, "🏁 تبریک! همه مراحل رو گذروندی!", reply_markup=get_main_menu())
        else:
            bot.send_message(message.chat.id, "➕ برای ادامه، دوباره «🎮 شروع بازی» رو بزن.", reply_markup=get_main_menu())
        return

    # منو
    if message.text == "👤 پروفایل":
        bot.send_message(message.chat.id,
            f"👤 نام: {user['name']}\n❤️ جان: {user['hearts']}\n🪙 سکه: {user['coins']}\n🏅 امتیاز: {user['score']}")
    elif message.text == "🎁 پاداش روزانه":
        now = time.time()
        if now - user["last_reward"] >= 86400:
            user["coins"] += 10
            user["last_reward"] = now
            save_data(data)
            bot.send_message(message.chat.id, "🎉 پاداش روزانه گرفتی: ۱۰ سکه!")
        else:
            remain = int(86400 - (now - user["last_reward"]))
            bot.send_message(message.chat.id, f"⏳ باید {remain//3600} ساعت و {(remain%3600)//60} دقیقه صبر کنی.")
    elif message.text == "🏆 برترین‌ها":
        top = sorted(data.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]
        res = "🏆 ۱۰ بازیکن برتر:\n\n"
        for i, (uid, u) in enumerate(top, 1):
            res += f"{i}. {u['name']} ➤ {u['score']} امتیاز\n"
        bot.send_message(message.chat.id, res)
    elif message.text == "👥 دعوت دوستان":
        ref_link = f"https://t.me/bagha_game_bot?start={user_id}"
        bot.send_message(message.chat.id, f"📨 لینک تو:\n{ref_link}\nهر دعوت = ۵۰ سکه 🎁")
    elif message.text == "🛒 فروشگاه":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("پرداخت ۴ ترون = ۱۰۰ سکه", url="https://tronscan.org"))
        markup.add(types.InlineKeyboardButton("🧾 ارسال فیش", callback_data="send_receipt"))
        markup.add(types.InlineKeyboardButton("❤️ خرید جان (۱۰۰ سکه)", callback_data="buy_heart"))
        bot.send_message(message.chat.id, f"💳 آدرس ترون:\n`{TRON_ADDRESS}`", parse_mode="Markdown", reply_markup=markup)
    elif message.text == "🎮 شروع بازی":
        if user["hearts"] < 3:
            bot.send_message(message.chat.id, "⚠️ برای شروع بازی باید حداقل ۳ جان داشته باشی. به فروشگاه برو و جان بخر.")
            return
        with open(questions_file, "r", encoding="utf-8") as f:
            questions = json.load(f)
        if user["current_q"] >= len(questions):
            bot.send_message(message.chat.id, "🏁 همه مراحل تموم شده!")
            return
        q = questions[user["current_q"]]
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for opt in q["options"]:
            kb.add(opt["text"])
        kb.add("🔙 بازگشت به منو")
        bot.send_message(message.chat.id, f"🧩 مرحله {user['current_q']+1}:\n\n{q['question']}", reply_markup=kb)
        user["step"] = "answering"
        save_data(data)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = load_data()
    user_id = str(call.message.chat.id)
    user = data.get(user_id)

    if call.data == "send_receipt":
        bot.send_message(call.message.chat.id, "🖼 لطفا تصویر یا متن فیش رو بفرست.")
        user["step"] = "awaiting_receipt"
        save_data(data)

    elif call.data == "buy_heart":
        if user["coins"] >= 100:
            user["coins"] -= 100
            user["hearts"] += 1
            save_data(data)
            bot.answer_callback_query(call.id, "❤️ یک جان اضافه خریدی!")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
            bot.send_message(call.message.chat.id, f"❤️ جان‌های شما: {user['hearts']}\n🪙 سکه‌ها: {user['coins']}")
        else:
            bot.answer_callback_query(call.id, "❌ سکه کافی نداری.")

    elif call.data.startswith("admin_"):
        # فرمت: admin_confirm_123456789 یا admin_reject_123456789
        parts = call.data.split("_")
        if len(parts) == 3 and user_id == str(ADMIN_ID):
            action = parts[1]
            target_id = parts[2]
            all_data = load_data()
            target = all_data.get(target_id)
            if not target:
                bot.answer_callback_query(call.id, "کاربر یافت نشد.")
                return

            if action == "confirm":
                target["coins"] = target.get("coins", 0) + 100
                save_data(all_data)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
                bot.send_message(call.message.chat.id, "✅ فیش تأیید شد و ۱۰۰ سکه به کاربر اضافه شد.")
                bot.send_message(int(target_id), "✅ فیش شما توسط ادمین تأیید شد و ۱۰۰ سکه به حساب شما اضافه شد.")
            elif action == "reject":
                save_data(all_data)
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
                bot.send_message(call.message.chat.id, "❌ فیش رد شد.")
                bot.send_message(int(target_id), "❌ فیش شما توسط ادمین رد شد. لطفا دوباره ارسال کن.")

@bot.message_handler(content_types=["photo", "text"])
def handle_receipt(message):
    user_id = str(message.chat.id)
    data = load_data()
    user = data.get(user_id)
    if not user:
        return

    if user.get("step") == "awaiting_receipt":
        # فیش رو به ادمین بفرست
        bot.send_message(ADMIN_ID, f"✅ فیش پرداخت از {user['name']} ({user_id}):")
        if message.photo:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        else:
            bot.send_message(ADMIN_ID, message.text)

        # دکمه تایید/رد برای ادمین
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ تأیید", callback_data=f"admin_confirm_{user_id}"))
        markup.add(types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{user_id}"))
        bot.send_message(ADMIN_ID, "لطفا وضعیت فیش را انتخاب کن:", reply_markup=markup)

        user["step"] = None
        save_data(data)
        bot.send_message(message.chat.id, "📤 فیش برای ادمین ارسال شد. منتظر تأیید باش.")

@app.route("/", methods=["GET"])
def index():
    return "ربات فعال است"

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

def set_webhook():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{API_TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=url)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    set_webhook()
