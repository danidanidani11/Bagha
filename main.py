import os
import json
import threading
from datetime import datetime, timedelta
from flask import Flask
import telebot
from telebot import types

# تنظیمات اصلی
app = Flask(__name__)
bot = telebot.TeleBot('7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew')
CHANNEL = '@bagha_game'
ADMIN_ID = '5542927340'  # آیدی ادمین (شما)
TRON_ADDRESS = 'TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb'

# --- توابع کمکی ---
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return {'users': {}, 'top': []}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def check_subscription(user_id):
    try:
        status = bot.get_chat_member(CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- سیستم عضویت و شروع ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    
    if not check_subscription(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL[1:]}"))
        markup.add(types.InlineKeyboardButton("عضو شدم ✅", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات باید در کانال ما عضو شوید:", reply_markup=markup)
        return
    
    data = load_data()
    if user_id not in data['users']:
        msg = bot.send_message(message.chat.id, "🎮 به بازی سقوط هواپیما خوش آمدید!\nلطفا نام بازیکن خود را وارد کنید:")
        bot.register_next_step_handler(msg, process_name)
    else:
        show_main_menu(message.chat.id)

def process_name(message):
    data = load_data()
    user_id = str(message.from_user.id)
    
    data['users'][user_id] = {
        'name': message.text,
        'coins': 50,  # سکه شروع
        'score': 0,
        'lives': 3,
        'last_daily': None,
        'invites': [],
        'invite_code': f"INVITE_{user_id[-6:]}"
    }
    save_data(data)
    
    bot.send_message(message.chat.id, f"✅ ثبت نام موفق!\nسلام {message.text}!\nشما 50 سکه شروع دریافت کردید.")
    show_main_menu(message.chat.id)

# --- منوی اصلی ---
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🏆 برترین‌ها", "🎮 شروع بازی")
    markup.add("🛒 فروشگاه", "📤 دعوت دوستان")
    markup.add("👤 پروفایل", "🎁 پاداش روزانه")
    bot.send_message(chat_id, "منوی اصلی:", reply_markup=markup)

# --- سیستم سوالات ---
questions = [
    {
        'q': 'چشمانت را باز می‌کنی... هواپیما سقوط کرده است. اولین کاری که می‌کنی چیست؟',
        'o': ['بررسی آسیب‌ها', 'فریاد کمک', 'جستجوی آب', 'فرار از محل'],
        'a': 0,
        'reward': 10,
        'penalty': 5
    },
    # سوالات دیگر...
]

@bot.message_handler(func=lambda m: m.text == "🎮 شروع بازی")
def start_game(message):
    data = load_data()
    user_id = str(message.from_user.id)
    
    if data['users'][user_id]['lives'] <= 0:
        bot.send_message(message.chat.id, "❌ جان شما تمام شده! از فروشگاه جان بخرید.")
        return
    
    send_question(message.chat.id, user_id, 0)

def send_question(chat_id, user_id, q_index):
    question = questions[q_index]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    for i, option in enumerate(question['o']):
        markup.add(f"{i+1}. {option}")
    
    markup.add("🔙 منوی اصلی")
    bot.send_message(chat_id, f"سوال {q_index+1}/{len(questions)}:\n{question['q']}", reply_markup=markup)

# --- فروشگاه ---
@bot.message_handler(func=lambda m: m.text == "🛒 فروشگاه")
def shop(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 خرید 100 سکه (4 TRX)", callback_data="buy_coins"))
    markup.add(types.InlineKeyboardButton("🩸 خرید جان (100 سکه)", callback_data="buy_life"))
    bot.send_message(message.chat.id, 
                    "🛍 فروشگاه:\n\n"
                    "• 100 سکه = 4 TRX\n"
                    f"آدرس TRX: `{TRON_ADDRESS}`\n\n"
                    "• 1 جان = 100 سکه",
                    reply_markup=markup,
                    parse_mode="Markdown")

# --- بقیه سیستم‌ها (پروفایل، برترین‌ها، دعوت دوستان، پاداش روزانه) ---
# [کدهای کامل در نسخه نهایی موجود است]

# --- اجرای برنامه ---
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    bot.infinity_polling(skip_pending=True)
