import os
import threading
from flask import Flask

# راه‌اندازی یک وب سرور ساده برای Render
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# اجرا در ترد جداگانه
threading.Thread(target=run_web).start()

import telebot, json, os, time, datetime
from telebot import types

bot = telebot.TeleBot('7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew')
admin_id = 5542927340
channel = 'bagha_game'
tron_address = 'TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb'

# سوالات بازی (لیست کامل)
questions = [
    {
        "q": "تو داخل یه جزیره متروک گیر افتادی. برای روشن نگه داشتن راه در شب چه‌کار می‌کنی؟",
        "o": ["آتش روشن می‌کنم", "منتظر روشنایی صبح می‌مونم", "منو 🔙"],
        "a": "آتش روشن می‌کنم",
        "d": "آتش گرما و نور فراهم می‌کند."
    },
    {
        "q": "بعد از روشن کردن آتش، صدایی از دریاچه می‌شنوی. به آب نزدیک می‌شی یا منتظر می‌مونی؟",
        "o": ["نزدیک می‌رم", "منتظر می‌مونم", "منو 🔙"],
        "a": "منتظر می‌مونم",
        "d": "منتظر بودن امنیت بیشتری فراهم می‌کنه."
    },
    {
        "q": "در صبح، دو راه پیش روته: مسیر جنگل انبوه یا ساحل کنار دریا. کدوم رو انتخاب می‌کنی؟",
        "o": ["جنگل انبوه", "ساحل", "منو 🔙"],
        "a": "ساحل",
        "d": "ساحل احتمال دارد کمک پیدا کنی."
    },
    {
        "q": "در ساحل، بقایای کشتی غرق‌شده‌ای هست. واردش می‌شی یا عبور می‌کنی؟",
        "o": ["واردش می‌م��", "عبور می‌کنم", "منو 🔙"],
        "a": "واردش می‌م",
        "d": "ممکنه منابع یا تجهیزات پیدا بشه."
    },
    {
        "q": "داخل کشتی، کمد چوبی قفل‌شده می‌بینی. بازش می‌کنی یا رد می‌شی؟",
        "o": ["بازش می‌کنم", "رد می‌شم", "منو 🔙"],
        "a": "بازش می‌کنم",
        "d": "ممکنه ابزار یا غذا داخل باشه."
    },
    {
        "q": "در کشتی، چراغ قوه داری یا باید راه نوری پیدا کنی؟",
        "o": ["چراغ قوه روشن می‌کنم", "با گوشی نور می‌گیرم", "منو 🔙"],
        "a": "چراغ قوه روشن می‌کنم",
        "d": "چراغ قوه مسیر رو روشن می‌کنه."
    },
    {
        "q": "چراغ قوه گیر افتاد. باید چه‌کار کنی؟",
        "o": ["باتری عوض کنم", "با نور گوشی ادامه می‌دم", "منو 🔙"],
        "a": "باتری عوض کنم",
        "d": "باتری تازه نور کافی می‌رسونه."
    },
    {
        "q": "در راه پله‌ای جنگلی، صدایی شبیه حیوان وحشی می‌شنوی. چه‌کار می‌کنی؟",
        "o": ["پنهان می‌شم", "فرار می‌کنم", "منو 🔙"],
        "a": "پنهان می‌شم",
        "d": "پنهان شدن امن‌تره."
    },
    {
        "q": "گرگ گرسنه می‌بینی که دنبالت میاد. واکنش؟",
        "o": ["آتش روشن می‌کنم", "فرار می‌کنم", "منو 🔙"],
        "a": "آتش روشن می‌کنم",
        "d": "گرگ از آتش می‌ترسه."
    },
    {
        "q": "راهت بازه اما طوفان در راهه. سرپناه می‌سازی یا ادامه می‌دی؟",
        "o": ["سرپناه می‌سازم", "ادامه می‌دم", "منو 🔙"],
        "a": "سرپناه می‌سازم",
        "d": "سرپناه امنیت ایجاد می‌کنه."
    },
    {
        "q": "سرپناه ساختی، ولی بارون شدید شروع شد. برای خشک‌کردن لباس‌ها چه‌کار می‌کنی؟",
        "o": ["لباس‌ها رو کنار آتش می‌ذارم", "توی کیسه می‌ذارم", "منو 🔙"],
        "a": "لباس‌ها رو کنار آتش می‌ذارم",
        "d": "گرما باعث خشک شدن سریع لباسه."
    },
    {
        "q": "صبح بعد طوفان، راهی جنگل می‌شی. دنبال چه می‌گردی؟",
        "o": ["آب سالم", "آذوقه", "منو 🔙"],
        "a": "آب سالم",
        "d": "آب اولین نیاز بقاءه."
    },
    {
        "q": "چشمه‌ای به نظر سالمه ولی نزدیکش مار هست. چه‌کار می‌کنی؟",
        "o": ["آرام نزدیک می‌شم", "مار رو تحریک می‌کنم", "منو 🔙"],
        "a": "آرام نزدیک می‌شم",
        "d": "هیس بودن خطر را کاهش می‌ده."
    },
    {
        "q": "در مسیر جنگل، چوب خشکی پیدا می‌کنی. چی می‌سازی؟",
        "o": ["چوب آتش‌زنه", "گرز", "منو 🔙"],
        "a": "چوب آتش‌زنه",
        "d": "آتش‌زنه برای روشنایی، حفاظت و پخت غذا ضروریه."
    },
    {
        "q": "در هنگام شکار ماهی در رودخانه، تور داری؟",
        "o": ["تور استفاده می‌کنم", "با دستانم می‌گیرم", "منو 🔙"],
        "a": "تور استفاده می‌کنم",
        "d": "تور شانس موفقیت رو بالا می‌بره."
    },
    {
        "q": "در شب دوم، صدای زمزمه در باد می‌شنوی. چه‌کار می‌کنی؟",
        "o": ["می‌رم بررسی کنم", "منتظر می‌مونم", "منو 🔙"],
        "a": "منتظر می‌مونم",
        "d": "منتظر موندن امن‌تره."
    },
    {
        "q": "یک نور قولنج مانند در دوردست دیدی. به سمتش می‌ری یا نه؟",
        "o": ["می‌رم", "نمی‌رم", "منو 🔙"],
        "a": "می‌رم",
        "d": "ممکنه کمک یا خطر باشه."
    },
    {
        "q": "چشمه‌ای می‌بینی که چشمک‌زن نور قرمز داره. می‌گیریش یا رد می‌شی؟",
        "o": ["می‌گیرم", "رد می‌شم", "منو 🔙"],
        "a": "رد می‌شم",
        "d": "نور عجیب ممکنه خطرناک باشه."
    },
    {
        "q": "ساعت شب، باد شدید می‌اد و صدای شلیک می‌شنوی. چه‌کار می‌کنی؟",
        "o": ["پنهان می‌شم", "آرام از کوچه عبور می‌کنم", "منو 🔙"],
        "a": "آرام از کوچه عبور می‌کنم",
        "d": "حرکت بی‌صدا احتمال ایمن بودن رو بالا می‌بره."
    },
    {
        "q": "در کوه‌پایه، سنگی بزرگ برای شکستن مواد غذایی می‌خوای بسازی؟",
        "o": ["بله می‌سازم", "نه لازم نیست", "منو 🔙"],
        "a": "بله می‌سازم",
        "d": "ابزار برای آماده‌سازی غذا ضروریه."
    },
    {
        "q": "در مسیر یخ زده، باید پاها رو گرم نگه‌داری. چه‌کار می‌کنی؟",
        "o": ["پارچه اضافه می‌پیچی", "پابرهنه ادامه می‌دم", "منو 🔙"],
        "a": "پارچه اضافه می‌پیچی",
        "d": "گرم نگه‌داشتن برای جلوگیری از سرمازدگیه."
    },
    {
        "q": "تو شب مه‌آلود بلندترین درخت رو دیدی. بالا می‌ری یا ادامه می‌دی؟",
        "o": ["بالا می‌رم", "ادامه می‌دم", "منو 🔙"],
        "a": "بالا می‌رم",
        "d": "بالا رفتن دید خوبی بهت می‌ده."
    },
    {
        "q": "صدای پرستو می‌شنوی که راهنماشه. دنبال می‌شی یا نه؟",
        "o": ["دنبال می‌شم", "نمی‌شم", "منو 🔙"],
        "a": "دنبال می‌شم",
        "d": "پرستوها اغلب بهبود مسیر نشون می‌دن."
    },
    {
        "q": "چاه قدیمی جلوته. می‌ری داخلش یا رد می‌شی؟",
        "o": ["می‌رم داخل", "رد می‌شم", "منو 🔙"],
        "a": "رد می‌شم",
        "d": "امکانات ریسک وجود داره."
    },
    {
        "q": "دو راه داری: یکی به‌طرف کوه آتش‌فشان و دیگری جنگل انبوه. انتخاب؟",
        "o": ["کوه", "جنگل", "منو 🔙"],
        "a": "جنگل",
        "d": "جنگل منابع بیشتری داره."
    },
    {
        "q": "در جنگل، چمچرایی یک هیزم‌شکن هست. بهش کمک می‌کنی؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "بله",
        "d": "همکاری ممکنه امنیت بیشتری بده."
    },
    {
        "q": "هیزم‌شکن نشانی از آب داره. دنبال می‌ری؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "بله",
        "d": "آب برای بقا ضروریه."
    },
    {
        "q": "پرنده‌ای زخمی روی زمین دیدی. نجاتش می‌دی؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "نه",
        "d": "شاید باعث اتلاف منابع شه."
    },
    {
        "q": "شب سرد، مواد غذایی ندارژی. چی کار می‌کنی؟",
        "o": ["آتش می‌زنم", "منتظر صبح می‌مونم", "منو 🔙"],
        "a": "آتش می‌زنم",
        "d": "آتش گرما و امنیت می‌ده."
    },
    {
        "q": "در میان سنگ‌ها، نور سبز دیدی. بررسی می‌کنی؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "بله",
        "d": "ممکنه فضای مرموزی باشه."
    },
    {
        "q": "دنبال غذا هستی، چه‌چیزی انتخاب می‌کنی؟",
        "o": ["قارچ جنگلی", "میوه‌های آویزون", "منو 🔙"],
        "a": "میوه‌های آویزون",
        "d": "میوه‌ها معمولاً کمتر سمّی هستن."
    },
    {
        "q": "اگر آتش خاموش شد، بازسازی می‌کنی یا دنبال مسیر می‌ری؟",
        "o": ["بازسازی می‌کنم", "مسیر می‌رم", "منو 🔙"],
        "a": "بازسازی می‌کنم",
        "d": "آتش امنیتت رو حفظ می‌کنه."
    },
    {
        "q": "تو تونل کوچک رسیدی، یه صدایی عجیبی شنیدی. جلو می‌ری؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "نه",
        "d": "پرهیز از خطر هوشمندانه‌ست."
    },
    {
        "q": "پس از رفتن از تونل، به پرتگاهی رسیدی. از جاده می‌ری یا صخره؟",
        "o": ["جاده", "صخره", "منو 🔙"],
        "a": "جاده",
        "d": "جاده معمولاً مسیر ایمن‌تریه."
    },
    {
        "q": "صدای وزش باد در گوشته. باز دین؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "نه",
        "d": "نترسیدن بهتره."
    },
    {
        "q": "در مسیر شبانه، نور مه‌آلود می‌بینی. می‌رسی؟",
        "o": ["بله", "نه", "منو 🔙"],
        "a": "نه",
        "d": "احتیاط واجبه."
    },
]

def load():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save(data):
    with open('users.json', 'w') as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data:
        data[uid] = {
            "name": "",
            "coins": 0,
            "score": 0,
            "life": 3,
            "step": 0,
            "last_daily": "",
            "waiting_receipt": False,
            "in_game": False
        }
        save(data)
    check_sub(m)

def check_sub(msg):
    try:
        status = bot.get_chat_member(f"@{channel}", msg.from_user.id).status
    except Exception:
        status = "left"
    if status in ["member", "administrator", "creator"]:
        ask_name(msg)
    else:
        link = f"https://t.me/{channel}"
        btn = types.InlineKeyboardMarkup()
        btn.add(types.InlineKeyboardButton("عضویت در کانال 📢", url=link))
        btn.add(types.InlineKeyboardButton("عضو شدم ✅", callback_data="check"))
        bot.send_message(msg.chat.id, "برای ادامه، لطفا عضو کانال شو:", reply_markup=btn)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    uid = str(c.from_user.id)
    data = load()
    if c.data == "check":
        try:
            status = bot.get_chat_member(f"@{channel}", c.from_user.id).status
        except Exception:
            status = "left"
        if status in ["member", "administrator", "creator"]:
            ask_name(c.message)
        else:
            bot.answer_callback_query(c.id, "⛔ هنوز عضو کانال نشدی!", show_alert=True)

    elif c.data == "buy_life":
        if data[uid]["coins"] >= 100:
            data[uid]["coins"] -= 100
            data[uid]["life"] += 1
            save(data)
            bot.edit_message_text("✅ جان خریداری شد!", c.message.chat.id, c.message.message_id)
        else:
            bot.answer_callback_query(c.id, "سکه کافی نداری!", show_alert=True)

    elif c.data.startswith('admin_'):
        if str(c.from_user.id) != str(admin_id):
            bot.answer_callback_query(c.id, "شما ادمین نیستید!", show_alert=True)
            return

        parts = c.data.split('_')
        action = parts[1]
        user_id = parts[2]

        if action == 'approve':
            data[user_id]['coins'] += 100
            save(data)
            bot.send_message(user_id, "✅ پرداخت شما تایید شد! 100 سکه به حساب شما اضافه شد.")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "تایید شد!")

        elif action == 'reject':
            bot.send_message(user_id, "❌ پرداخت شما رد شد!")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "رد شد!")

def ask_name(msg):
    bot.send_message(msg.chat.id, "👤 لطفا اسمت رو بفرست:")
    bot.register_next_step_handler(msg, save_name)

def save_name(m):
    data = load()
    uid = str(m.from_user.id)
    data[uid]["name"] = m.text
    save(data)
    main_menu(m.chat.id)

def main_menu(cid):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎮 شروع بازی", "🛒 فروشگاه")
    kb.add("📊 پروفایل", "🏆 برترین‌ها", "🎁 پاداش روزانه")
    bot.send_message(cid, "از منو یکی رو انتخاب کن:", reply_markup=kb)

def send_question(chat_id, step):
    data = load()
    uid = str(chat_id)
    data[uid]["in_game"] = True
    save(data)
    q = questions[step]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in q["o"]:
        kb.add(opt)
    bot.send_message(chat_id, f"🧩 مرحله {step + 1}:\n{q['q']}", reply_markup=kb)

@bot.message_handler(content_types=["text"])
def handle_text(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data:
        return
    u = data[uid]

    if u.get("waiting_receipt"):
        if m.text == "منو 🔙":
            u["waiting_receipt"] = False
            save(data)
            return main_menu(m.chat.id)
        else:
            bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
            u["waiting_receipt"] = False
            save(data)
            txt = f"📥 رسید جدید\nنام: {u['name']}\nID: {uid}\n📝 متن: {m.text}"
            markup = types.InlineKeyboardMarkup()
            markup.row(
                types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_approve_{uid}"),
                types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{uid}")
            )
            bot.send_message(admin_id, txt, reply_markup=markup)
            return

    if m.text == "🎮 شروع بازی":
        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ جان‌هات تموم شده! لطفا از فروشگاه جان بخر.")
            return
        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
        send_question(m.chat.id, u["step"])
        return

    if m.text == "منو 🔙":
        u["in_game"] = False
        save(data)
        return main_menu(m.chat.id)

    if u["in_game"] and u["step"] < len(questions) and m.text in questions[u["step"]]["o"]:
        if m.text == questions[u["step"]]["a"]:
            u["score"] += 1
            u["coins"] += 5
            bot.send_message(m.chat.id, "✅ جواب درست بود! مرحله بعدی.")
        else:
            u["life"] -= 1
            bot.send_message(m.chat.id, f"❌ جواب اشتباه بود: {questions[u['step']]['d']}")
        u["step"] += 1
        save(data)

        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ جان‌هات تموم شد! لطفا از فروشگاه جان بخر.")
            u["in_game"] = False
            save(data)
            return

        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
            bot.send_message(m.chat.id, "🎉 تبریک! همه مراحل رو تموم کردی. دوباره شروع کن.")

        time.sleep(1)
        send_question(m.chat.id, u["step"])
        return

    elif m.text == "📊 پروفایل":
        bot.send_message(m.chat.id, f"""🧍‍♂️ نام: {u['name']}
❤️ جان: {u['life']}
💰 سکه: {u['coins']}
🏅 امتیاز: {u['score']}""")

    elif m.text == "🎁 پاداش روزانه":
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if u.get("last_daily") == now:
            bot.send_message(m.chat.id, "⛔ امروز پاداش گرفتی، فردا بیا.")
        else:
            u["coins"] += 10
            u["last_daily"] = now
            save(data)
            bot.send_message(m.chat.id, "🎉 پاداش روزانه ۱۰ سکه به حسابت اضافه شد!")

    elif m.text == "🛒 فروشگاه":
        u["in_game"] = False
        save(data)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🩸 خرید جان (۱۰۰ سکه)", callback_data="buy_life"))
        kb.add(types.InlineKeyboardButton("💳 پرداخت ترون", url="https://tronscan.org"))
        bot.send_message(m.chat.id, "🛍 فروشگاه:", reply_markup=kb)

@bot.message_handler(content_types=["photo"])
def handle_photo(m):
    data = load()
    uid = str(m.from_user.id)
    u = data.get(uid)
    if not u:
        return

    if u.get("waiting_receipt"):
        bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
        u["waiting_receipt"] = False
        save(data)
        txt = f"📥 رسید جدید\nنام: {u['name']}\nID: {uid}"
        if m.caption:
            txt += f"\n📝 متن: {m.caption}"
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_approve_{uid}"),
            types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{uid}")
        )
        bot.send_photo(admin_id, m.photo[-1].file_id, caption=txt, reply_markup=markup)
      
bot.polling()
