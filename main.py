import os
import json
import time
import threading
from datetime import datetime, timedelta
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
            "id": i,
            "question": f"✈️ مرحله {i} - هواپیمای شما سقوط کرده. در جنگل بیدار شدید...",
            "options": [
                {"text": "بررسی اطراف برای غذا", "correct": True, "reason": "در مراحل اولیه بقا، غذا مهم‌ترین نیاز است"},
                {"text": "تلاش برای تماس اضطراری", "correct": False, "reason": "دستگاه‌های ارتباطی معمولاً بعد از سقوط کار نمی‌کنند"},
                {"text": "پنهان شدن تا شب", "correct": False, "reason": "شب شدن ممکن است خطرناک‌تر باشد"},
                {"text": "رفتن به دل جنگل", "correct": False, "reason": "بدون تجهیزات گم خواهید شد"}
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
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def get_main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("🎮 شروع بازی", "🏆 برترین‌ها", "🛒 فروشگاه", "👥 دعوت دوستان", "👤 پروفایل", "🎁 پاداش روزانه")
    return kb

# --- سیستم عضویت ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    data = load_data()

    if not check_membership(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
        markup.add(types.InlineKeyboardButton("✅ تایید عضویت", callback_data="verify_membership"))
        bot.send_message(message.chat.id, "برای استفاده از ربات، لطفاً در کانال ما عضو شوید و سپس روی دکمه تایید عضویت کلیک کنید:", reply_markup=markup)
        return

    if user_id not in data:
        bot.send_message(message.chat.id, "👋 به بازی ماجراجویی خوش آمدید! لطفاً نام بازیکن خود را وارد کنید:")
        data[user_id] = {"step": "get_name"}
        save_data(data)
    else:
        bot.send_message(message.chat.id, f"سلام {data[user_id]['name']}! منوی اصلی:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: call.data == "verify_membership")
def verify_membership(call):
    if check_membership(call.message.chat.id):
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "شما هنوز در کانال عضو نشده‌اید!", show_alert=True)

# --- سیستم فروشگاه ---
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
        f"موجودی شما: {data.get(user_id, {}).get('coins', 0)} سکه | {data.get(user_id, {}).get('hearts', 0)} ❤️",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["buy_coins", "buy_heart"])
def handle_purchase(call):
    user_id = str(call.message.chat.id)
    data = load_data()
    
    if call.data == "buy_coins":
        data[user_id]["step"] = "awaiting_payment"
        save_data(data)
        bot.send_message(
            call.message.chat.id,
            "💰 برای خرید 100 سکه:\n\n"
            f"1. مبلغ 4 TRX به آدرس زیر واریز کنید:\n`{TRON_ADDRESS}`\n"
            "2. سپس رسید پرداخت را ارسال کنید.",
            parse_mode="Markdown"
        )
    elif call.data == "buy_heart":
        if data[user_id]["coins"] >= 100:
            data[user_id]["coins"] -= 100
            data[user_id]["hearts"] += 1
            save_data(data)
            bot.send_message(call.message.chat.id, "✅ 1 جان با موفقیت خریداری شد!")
        else:
            bot.send_message(call.message.chat.id, "❌ سکه کافی ندارید!")
    
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=["photo", "text"])
def handle_payment(message):
    user_id = str(message.chat.id)
    data = load_data()
    
    if data.get(user_id, {}).get("step") == "awaiting_payment":
        # ارسال رسید به ادمین برای تایید
        admin_markup = types.InlineKeyboardMarkup()
        admin_markup.row(
            types.InlineKeyboardButton("✅ تایید پرداخت", callback_data=f"approve_{user_id}"),
            types.InlineKeyboardButton("❌ رد پرداخت", callback_data=f"reject_{user_id}")
        )
        
        if message.photo:
            bot.send_photo(
                ADMIN_ID,
                message.photo[-1].file_id,
                caption=f"رسید پرداخت از {data[user_id].get('name', 'ناشناس')} ({user_id})",
                reply_markup=admin_markup
            )
        else:
            bot.send_message(
                ADMIN_ID,
                f"رسید پرداخت از {data[user_id].get('name', 'ناشناس')} ({user_id}):\n\n{message.text}",
                reply_markup=admin_markup
            )
        
        data[user_id]["step"] = None
        save_data(data)
        bot.send_message(message.chat.id, "✅ رسید شما برای بررسی ارسال شد. پس از تایید ادمین، سکه‌ها به حساب شما اضافه می‌شوند.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def handle_admin_decision(call):
    if str(call.from_user.id) != str(ADMIN_ID):
        bot.answer_callback_query(call.id, "شما مجاز به انجام این کار نیستید!", show_alert=True)
        return
    
    action, user_id = call.data.split("_")
    data = load_data()
    
    if action == "approve":
        data[user_id]["coins"] += 100
        save_data(data)
        bot.send_message(user_id, "✅ پرداخت شما تایید شد! 100 سکه به حساب شما اضافه شد.")
        bot.answer_callback_query(call.id, "پرداخت تایید شد!")
    else:
        bot.send_message(user_id, "❌ پرداخت شما رد شد. در صورت نیاز با پشتیبانی تماس بگیرید.")
        bot.answer_callback_query(call.id, "پرداخت رد شد!")
    
    # حذف دکمه‌های تایید/رد
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

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
    
    current_question = data[user_id].get("current_question", 0)
    
    if current_question >= len(questions):
        bot.send_message(message.chat.id, "🎉 شما تمام مراحل را کامل کرده‌اید!")
        return
    
    question = questions[current_question]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for option in question["options"]:
        markup.add(option["text"])
    
    markup.add("🔙 بازگشت به منو")
    
    bot.send_message(
        message.chat.id,
        f"🧩 مرحله {current_question + 1}/{len(questions)}:\n\n{question['question']}",
        reply_markup=markup
    )
    
    data[user_id]["step"] = "answering"
    save_data(data)

# --- وب‌هوک و اجرا ---
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Bad request', 400

@app.route('/')
def index():
    return 'Bot is running!', 200

def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{API_TOKEN}"
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    print(f"Webhook set to: {webhook_url}")

if __name__ == '__main__':
    if os.environ.get('RENDER'):
        set_webhook()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
