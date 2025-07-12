import os
import json
import time
import threading
from flask import Flask, request
import telebot
from telebot import types

# تنظیمات اصلی
API_TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
CHANNEL_USERNAME = "@bagha_game"
ADMIN_ID = 5542927340
TRON_ADDRESS = "TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# فایل‌های دیتابیس
data_file = "users.json"
questions_file = "questions.json"

# ایجاد فایل‌ها اگر وجود ندارند
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

# --- توابع کمکی ---
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

# --- سیستم عضویت ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    data = load_data()

    if not check_membership(message.chat.id):
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        join_btn.add(types.InlineKeyboardButton("✅ تایید عضویت", callback_data="check_membership"))
        bot.send_message(message.chat.id, "🔒 برای استفاده از ربات، ابتدا عضو کانال شوید و سپس روی تایید عضویت کلیک کنید.", reply_markup=join_btn)
        return

    if user_id not in data:
        bot.send_message(message.chat.id, "👋 خوش آمدید! لطفاً نام بازیکن خود را وارد کنید:")
        data[user_id] = {"step": "get_name"}
        save_data(data)
        return

    bot.send_message(message.chat.id, f"سلام {data[user_id]['name']} 👋", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_membership_callback(call):
    if check_membership(call.message.chat.id):
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "هنوز در کانال عضو نشدید!", show_alert=True)

# --- سیستم فروشگاه و پرداخت ---
@bot.message_handler(func=lambda m: m.text == "🛒 فروشگاه")
def shop(message):
    user_id = str(message.chat.id)
    data = load_data()
    
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("💳 خرید 100 سکه (4 TRX)", callback_data="buy_coins"),
        types.InlineKeyboardButton("❤️ خرید جان (100 سکه)", callback_data="buy_heart")
    )
    
    bot.send_message(
        message.chat.id,
        f"🛍 فروشگاه:\n\n"
        f"• 100 سکه = 4 TRX\n"
        f"آدرس TRX: `{TRON_ADDRESS}`\n\n"
        f"• 1 جان = 100 سکه\n\n"
        f"موجودی شما: {data.get(user_id, {}).get('coins', 0)} سکه",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["buy_coins", "buy_heart"])
def handle_payment(call):
    user_id = str(call.message.chat.id)
    data = load_data()
    
    if call.data == "buy_coins":
        bot.send_message(
            call.message.chat.id,
            "💰 برای خرید 100 سکه:\n\n"
            f"1. مبلغ 4 TRX به آدرس زیر واریز کنید:\n`{TRON_ADDRESS}`\n"
            "2. سپس رسید پرداخت را ارسال کنید.",
            parse_mode="Markdown"
        )
        data[user_id]["step"] = "awaiting_payment"
        save_data(data)
    elif call.data == "buy_heart":
        if data.get(user_id, {}).get("coins", 0) >= 100:
            data[user_id]["coins"] -= 100
            data[user_id]["hearts"] += 1
            save_data(data)
            bot.send_message(call.message.chat.id, "✅ 1 جان با موفقیت خریداری شد!")
        else:
            bot.send_message(call.message.chat.id, "❌ سکه کافی ندارید!")

    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=["photo", "text"])
def handle_receipt(message):
    user_id = str(message.chat.id)
    data = load_data()
    
    if data.get(user_id, {}).get("step") == "awaiting_payment":
        # ارسال به ادمین برای تایید
        admin_markup = types.InlineKeyboardMarkup()
        admin_markup.row(
            types.InlineKeyboardButton("✅ تایید پرداخت", callback_data=f"approve_{user_id}"),
            types.InlineKeyboardButton("❌ رد پرداخت", callback_data=f"reject_{user_id}")
        )
        
        if message.photo:
            bot.send_photo(
                ADMIN_ID, 
                message.photo[-1].file_id, 
                caption=f"رسید پرداخت از کاربر {data[user_id].get('name', 'ناشناس')} ({user_id})",
                reply_markup=admin_markup
            )
        else:
            bot.send_message(
                ADMIN_ID,
                f"رسید پرداخت از کاربر {data[user_id].get('name', 'ناشناس')} ({user_id}):\n\n{message.text}",
                reply_markup=admin_markup
            )
        
        data[user_id]["step"] = None
        save_data(data)
        bot.send_message(message.chat.id, "✅ رسید شما برای ادمین ارسال شد. پس از تایید، سکه‌ها به حساب شما اضافه می‌شود.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def handle_admin_decision(call):
    action, user_id = call.data.split("_")
    
    if str(call.from_user.id) != str(ADMIN_ID):
        bot.answer_callback_query(call.id, "شما مجاز به این کار نیستید!", show_alert=True)
        return
    
    data = load_data()
    
    if action == "approve":
        data[user_id]["coins"] += 100
        save_data(data)
        bot.send_message(user_id, "✅ پرداخت شما تایید شد! 100 سکه به حساب شما اضافه شد.")
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.answer_callback_query(call.id, "پرداخت تایید شد!")
    else:
        bot.send_message(user_id, "❌ پرداخت شما رد شد. در صورت مشکل با پشتیبانی تماس بگیرید.")
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.answer_callback_query(call.id, "پرداخت رد شد!")

# --- سیستم بازی ---
@bot.message_handler(func=lambda m: m.text == "🎮 شروع بازی")
def start_game(message):
    user_id = str(message.chat.id)
    data = load_data()
    
    if user_id not in data:
        bot.send_message(message.chat.id, "لطفاً ابتدا /start را بزنید.")
        return
    
    if data[user_id].get("hearts", 0) <= 0:
        bot.send_message(message.chat.id, "❌ جان شما تمام شده! از فروشگاه جان خریداری کنید.")
        return
    
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    current_q = data[user_id].get("current_q", 0)
    
    if current_q >= len(questions):
        bot.send_message(message.chat.id, "🎉 شما تمام مراحل را کامل کرده‌اید!")
        return
    
    question = questions[current_q]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for option in question["options"]:
        markup.add(option["text"])
    
    markup.add("🔙 بازگشت به منو")
    
    bot.send_message(
        message.chat.id,
        f"🧩 مرحله {current_q + 1}/{len(questions)}:\n\n{question['question']}",
        reply_markup=markup
    )
    
    data[user_id]["step"] = "answering"
    save_data(data)

# --- بقیه توابع (پروفایل، برترین‌ها، دعوت دوستان، پاداش روزانه) ---
# [کدهای کامل در نسخه نهایی موجود است]

# --- اجرای برنامه ---
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    # تنظیم وب‌هوک برای Render
    def set_webhook():
        url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{API_TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=url)
    
    threading.Thread(target=run_flask).start()
    set_webhook()
