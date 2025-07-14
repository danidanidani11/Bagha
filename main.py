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

# ✅ بارگذاری سوالات از فایل یا ساخت اولیه
if not os.path.exists(QUESTIONS_FILE):
  
sample_questions = [
    {"question": "✈️ [مرحله 1] هواپیما سقوط کرده و شما در جنگلی تاریک هستید. اولین واکنش شما چیست؟", "options": ["🏃 فرار می‌کنم", "🧭 نقشه می‌کشم", "🔥 آتش روشن می‌کنم", "😱 تسلیم می‌شوم"], "answer": 2, "explanations": {"0": "فرار بدون هدف ممکن است باعث گم‌شدگی بیشتر شود.", "1": "نقشه کشیدن بدون دید کافی بی‌فایده است.", "2": "✅ روشن کردن آتش باعث دیده شدن توسط تیم نجات می‌شود.", "3": "تسلیم شدن به معنای پایان تلاش برای بقا است."}},
    {"question": "🌘 [مرحله 2] هوا در حال تاریک شدن است و هنوز پناهگاهی ندارید. چه می‌کنید؟", "options": ["🪓 شروع به ساخت پناهگاه می‌کنم", "🔥 آتش روشن نگه می‌دارم", "🏃 به مسیر ادامه می‌دهم", "🪵 برگ جمع می‌کنم"], "answer": 0, "explanations": {"0": "✅ داشتن پناهگاه در شب اولویت است.", "1": "آتش مفید است اما بدون پناهگاه کافی نیست.", "2": "شب‌گردی خطرناک است.", "3": "برگ‌ها بخشی از پناهگاه‌اند اما کافی نیستند."}},
    {"question": "💧 [مرحله 3] تشنه‌ای و منبع آبی می‌یابی، ولی بو و رنگ آن مشکوک است. چه می‌کنی؟", "options": ["🥤 مستقیم می‌نوشم", "🧪 آزمایش می‌کنم", "🔥 آن را می‌جوشانم", "🚶‍♂️ به مسیر ادامه می‌دهم"], "answer": 2, "explanations": {"0": "نوشیدن مستقیم ممکن است منجر به بیماری شود.", "1": "آزمایش در شرایط بقا دشوار است.", "2": "✅ جوشاندن آب ساده‌ترین روش تصفیه است.", "3": "ادامه دادن با تشنگی خطرناک است."}},
    {"question": "🦴 [مرحله 4] استخوان‌هایی در نزدیکی می‌یابی. واکنش منطقی چیست؟", "options": ["😱 وحشت می‌کنم", "🔍 اطراف را بررسی می‌کنم", "🏃 فرار می‌کنم", "📷 عکس می‌گیرم"], "answer": 1, "explanations": {"0": "وحشت فایده‌ای ندارد.", "1": "✅ بررسی محل می‌تواند علت و خطر را مشخص کند.", "2": "فرار کورکورانه خطرناک است.", "3": "عکس گرفتن اولویت ندارد."}},
    {"question": "🌲 [مرحله 5] صدای خش‌خش از پشت درختان می‌آید. چه می‌کنی؟", "options": ["🧍 بی‌حرکت می‌مانم", "📢 فریاد می‌زنم", "🔦 با نور بررسی می‌کنم", "🏃 فرار می‌کنم"], "answer": 2, "explanations": {"0": "بی‌حرکت ماندن کمک می‌کند اما کافی نیست.", "1": "فریاد زدن ممکن است خطر را تحریک کند.", "2": "✅ نور کمک می‌کند بفهمی چه چیزی در آنجاست.", "3": "فرار ممکن است توجه بیشتری جلب کند."}},
    {"question": "🍄 [مرحله 6] قارچ‌هایی دیده‌ای که شبیه قارچ‌های سمی هستند. چه می‌کنی؟", "options": ["🌿 می‌خورم چون گرسنه‌ام", "🤢 دورشان می‌اندازم", "🧠 بررسی می‌کنم و مقایسه می‌کنم", "🔥 می‌سوزانم"], "answer": 2, "explanations": {"0": "خوردن قارچ ناشناس بسیار خطرناک است.", "1": "دور ریختن عجولانه است.", "2": "✅ بررسی دقیق ممکن است کمک کند تشخیص دهی.", "3": "سوزاندن بی‌دلیل اتلاف منابع است."}},
    {"question": "🛖 [مرحله 7] پناهگاه شما با باران فرو ریخته. چه کار می‌کنید؟", "options": ["🪵 پناهگاه را تعمیر می‌کنم", "☔ زیر درخت پناه می‌گیرم", "🔥 فقط آتش روشن می‌کنم", "🏃 به دنبال جای جدید می‌گردم"], "answer": 0, "explanations": {"0": "✅ بازسازی سریع مهم‌ترین کار است.", "1": "درخت ممکن است در طوفان خطرناک باشد.", "2": "آتش به‌تنهایی کافی نیست.", "3": "جابه‌جایی در باران خطرناک است."}},
    {"question": "🐾 [مرحله 8] ردپای حیوانی بزرگ اطراف کمپ می‌بینی. چه واکنشی نشان می‌دهی؟", "options": ["🐻 به‌دنبال حیوان می‌گردم", "🚫 اطراف کمپ را بررسی می‌کنم", "🏃 از کمپ فرار می‌کنم", "📦 وسایل را جمع می‌کنم و می‌روم"], "answer": 1, "explanations": {"0": "به‌دنبال حیوان رفتن خطرناک است.", "1": "✅ بررسی اطراف برای اطمینان از امنیت ضروری است.", "2": "فرار بدون هدف خطرناک است.", "3": "ترک محل بدون برنامه عجولانه است."}},
    {"question": "📻 [مرحله 9] رادیویی قدیمی در لاشه هواپیما پیدا می‌کنی. چه می‌کنی؟", "options": ["🔋 باتری آن را بررسی می‌کنم", "📻 روشنش می‌کنم", "🪓 آن را می‌شکنم", "🛑 بی‌خیال می‌شوم"], "answer": 0, "explanations": {"0": "✅ باتری مهم‌ترین بخش برای عملکرد رادیو است.", "1": "روشن کردن بدون باتری ممکن نیست.", "2": "شکستن آن، شانس کمک را از بین می‌برد.", "3": "نادیده گرفتن آن فرصت نجات را کاهش می‌دهد."}},
    {"question": "🧭 [مرحله 10] نقشه‌ای نصفه در کوله‌پشتی پیدا می‌کنی. چه می‌کنی؟", "options": ["🧠 با ذهنم تکمیلش می‌کنم", "🗺️ از آن استفاده نمی‌کنم", "🔍 ترکیبش می‌کنم با مسیرهایی که دیده‌ام", "🛑 آن را پنهان می‌کنم"], "answer": 2, "explanations": {"0": "فرضیات ذهنی بدون اطلاعات دقیق خطرناک‌اند.", "1": "نادیده گرفتن نقشه نادیده گرفتن فرصت است.", "2": "✅ ترکیب نقشه با اطلاعات مشاهداتی بهترین راه استفاده از آن است.", "3": "پنهان‌کردن فایده‌ای ندارد."}},
    ...
    # مراحل 11 تا 100 دقیقاً به همین صورت ادامه دارند
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

def check_name(m):
    users = load_users()
    user_id = str(m.chat.id)
    
    # اگر پیام /start بود، اجازه دهید پردازش شود
    if m.text and m.text.startswith('/start'):
        return True
    
    # بررسی وجود کاربر و نام
    return user_id in users and "name" in users[user_id] and users[user_id]["name"].strip() != ""
    
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

@bot.message_handler(func=lambda m: m.reply_to_message and "نام خود را وارد کن" in m.reply_to_message.text)
def process_name(m):
    text = m.text or ""
    if text.startswith("/"):
        bot.send_message(m.chat.id, "❗️نام معتبر نیست. لطفاً فقط نام خود را وارد کنید:")
        return

    users = load_users()
    users[str(m.chat.id)]["name"] = text.strip()
    save_users(users)
    bot.send_message(m.chat.id, f"✅ ثبت شد: {text.strip()}", reply_markup=main_menu())
@bot.message_handler(commands=['start'])
def handle_start(m):
    user_id = str(m.chat.id)
    users = load_users()
    
    # بررسی عضویت در کانال
    if not is_member(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
        bot.send_message(user_id, "📛 برای استفاده از ربات، ابتدا باید در کانال عضو شوید:", reply_markup=markup)
        return
    
    # ایجاد کاربر جدید اگر وجود ندارد
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
    
    # اگر نام کاربر خالی است
    if not users[user_id]["name"]:
        msg = bot.send_message(user_id, "👤 لطفاً نام واقعی خود را وارد کنید (حداقل 2 حرف):", 
                             reply_markup=types.ForceReply(selective=True))
        bot.register_next_step_handler(msg, process_name)  # اینجا تابع process_name فراخوانی می‌شود
    else:
        bot.send_message(user_id, f"🔹 سلام {users[user_id]['name']}!", reply_markup=main_menu())

# 🎮 بازی
@bot.message_handler(func=lambda m: m.text == "🎮 شروع بازی")
def start_game(m):
    user_id = str(m.chat.id)
    users = load_users()

    if user_id not in users:
        bot.send_message(m.chat.id, "❗️ ابتدا باید ثبت‌نام کنید. /start")
        return

    user = users[user_id]
    user.setdefault("step", 0)  # مقدار پیش‌فرض اگر وجود نداشته باشد
    user.setdefault("life", 3)
    user.setdefault("coin", 0)
    user.setdefault("score", 0)

    # ذخیره تغییرات اولیه
    save_users(users)

    # بارگذاری سوالات
    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)

    # بررسی اگر کاربر تمام مراحل را گذرانده باشد
    if user["step"] >= len(questions):
        bot.send_message(m.chat.id, "🎉 شما تمام مراحل را کامل کرده‌اید! به زودی مراحل جدید اضافه خواهد شد.")
        return

    # ارسال سوال از مرحله‌ای که کاربر قبلاً رسیده بود
    q = questions[user["step"]]
    markup = types.InlineKeyboardMarkup()
    for i, opt in enumerate(q["options"]):
        markup.add(types.InlineKeyboardButton(opt, callback_data=f"q_{i}"))

    bot.send_message(m.chat.id, f"{q['question']}", reply_markup=markup)

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
    # بررسی تطابق دقیق متن پیام با گزینه‌ها (با حذف فاصله‌های اضافی)
    return any(m.text.strip() == opt.strip() for opt in q["options"])

@bot.message_handler(func=is_valid_answer)
def answer_question(m):
    users = load_users()
    user = users[str(m.chat.id)]
    step = user["step"]

    q = questions[step]
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

    if user["step"] < len(questions):
        send_question(m.chat.id)
    else:
        bot.send_message(m.chat.id, "🏁 تمام مراحل به پایان رسید!")

@bot.message_handler(func=lambda m: m.text == "🔙 بازگشت به منو")
def back_to_menu(m):
    bot.send_message(m.chat.id, "↩️ بازگشت به منو", reply_markup=main_menu())

# 🛒 فروشگاه - منو
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
@bot.message_handler(content_types=['photo'])
def handle_photo_payment(m):
    # بررسی کن که آیا این عکس پاسخ به پیام درخواست فیش است
    if m.reply_to_message and "فیش" in m.reply_to_message.text and m.text != "💳 ارسال فیش پرداخت":
        file_id = m.photo[-1].file_id
        caption = f"📥 فیش پرداخت تصویری از {m.from_user.first_name}"
        bot.send_photo(ADMIN_ID, file_id, caption=caption, reply_markup=payment_markup(m.chat.id))
    else:
        bot.send_message(m.chat.id, "📸 لطفاً فیش پرداخت را به صورت *عکس* یا *متن* ارسال کن:", reply_markup=types.ForceReply(selective=True), parse_mode="Markdown")
# 📤 دریافت فیش پرداخت و ارسال برای ادمین
@bot.message_handler(func=lambda m: m.reply_to_message and "فیش" in m.reply_to_message.text and m.text != "💳 ارسال فیش پرداخت")
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
    user_id = str(m.chat.id)
    
    if user_id not in users:
        bot.send_message(m.chat.id, "❌ خطا در یافتن اطلاعات کاربر. لطفاً با /start مجدداً شروع کنید.")
        return
    
    user = users[user_id]
    now = datetime.datetime.now()
    
    # اگر last_bonus وجود ندارد یا خالی است
    if "last_bonus" not in user or not user["last_bonus"]:
        user["last_bonus"] = "2000-01-01 00:00:00"
    
    try:
        last = datetime.datetime.strptime(user["last_bonus"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        last = datetime.datetime.min
        user["last_bonus"] = "2000-01-01 00:00:00"
    
    delta = now - last
    
    # تغییر به 12 ساعت (43200 ثانیه)
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

@bot.message_handler(func=lambda m: True)
def block_if_no_name(m):
    if not check_name(m):
        if m.text != "/start":
            bot.send_message(m.chat.id, "❗️ لطفاً ابتدا نام خود را وارد کنید. /start")

def get_user_step(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("step", -1)

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
        
        # اضافه کردن گزینه‌ها با شماره
        for i, opt in enumerate(q["options"]):
            markup.add(f"{i+1}. {opt}")
            
        markup.add("🔙 بازگشت به منو")
        bot.send_message(chat_id, q["question"], reply_markup=markup)
    else:
        bot.send_message(chat_id, "🎉 شما همه مراحل را کامل کردید! به زودی مراحل جدید اضافه خواهد شد.")
def is_valid_answer(m):
    users = load_users()
    user = users.get(str(m.chat.id))
    if not user:
        return False

    step = user.get("step", -1)
    if step < 0 or step >= len(questions):  # توجه: questions همون لیست سوالاته
        return False

    q = questions[step]
    return m.text.strip() in q["options"]
    # بررسی آیا متن پیام با یکی از گزینه‌ها مطابقت دارد
    return any(m.text.strip() == opt for opt in q["options"])

@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    # اجازه پردازش /start در هر حالت
    if m.text and m.text.startswith('/start'):
        return
        
    users = load_users()
    user_id = str(m.chat.id)
    
    # بررسی آیا کاربر ثبت نام کرده است
    if user_id not in users or not users[user_id].get("name"):
        bot.send_message(m.chat.id, "❗️ لطفاً ابتدا با دستور /start ثبت نام کنید.")
        return
        
    # اگر پیام مربوط به بازی است
    if is_valid_answer(m):
        answer_question(m)
        return
        
    # سایر پیام‌ها
    bot.send_message(m.chat.id, "⚠️ لطفاً از منوی اصلی انتخاب کنید.", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data.startswith("q_"))
def handle_question_answer(call):
    chat_id = call.message.chat.id
    user_id = str(chat_id)

    # بارگذاری اطلاعات کاربر و سوالات
    users = load_users()
    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)

    user = users.get(user_id)
    if not user:
        bot.answer_callback_query(call.id, "❌ خطا در یافتن اطلاعات کاربر.")
        return

    current_step = user.get("step", 0)
    if current_step >= len(questions):
        bot.answer_callback_query(call.id, "✅ شما تمام مراحل را گذرانده‌اید!")
        return

    question = questions[current_step]
    selected_option = int(call.data.split("_")[1])
    correct = selected_option == question["answer"]

    # ساخت متن توضیحات
    explanation_text = ""
    for idx, opt in enumerate(question["options"]):
        mark = "✅" if idx == question["answer"] else ("❌" if idx == selected_option else "▫️")
        explanation_text += f"{mark} {opt}\n— {question['explanations'].get(idx, '')}\n\n"

    # بروزرسانی اطلاعات کاربر
    if correct:
        user["score"] += 20
        user["coin"] += 10
        result_message = "✅ پاسخ درست! +۲۰ امتیاز و +۱۰ سکه."
    else:
        user["score"] += 5
        user["life"] -= 1
        result_message = "❌ پاسخ اشتباه! +۵ امتیاز و -۱ جان."

    # افزایش مرحله فقط اگر کاربر هنوز جان دارد
    if user["life"] > 0:
        user["step"] += 1
    else:
        bot.send_message(chat_id, "💔 جان شما تمام شد! برای ادامه، جان خریداری کنید.", reply_markup=main_menu())

    # ذخیره تغییرات
    save_users(users)

    # نمایش نتیجه به کاربر
    bot.edit_message_text(
        f"{result_message}\n\n📝 توضیحات:\n{explanation_text}",
        chat_id,
        call.message.message_id
    )

    # ارسال سوال بعدی اگر کاربر جان دارد و مرحله تمام نشده باشد
    if user["life"] > 0 and user["step"] < len(questions):
        next_q = questions[user["step"]]
        markup = types.InlineKeyboardMarkup()
        for i, opt in enumerate(next_q["options"]):
            markup.add(types.InlineKeyboardButton(opt, callback_data=f"q_{i}"))
        bot.send_message(chat_id, f"{next_q['question']}", reply_markup=markup)
    elif user["step"] >= len(questions):
        bot.send_message(chat_id, "🎉 تبریک! شما تمام مراحل را کامل کردید!")
            
if __name__ == "__main__":
    Thread(target=run).start()
