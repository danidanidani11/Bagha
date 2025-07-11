import telebot

# توکن رباتت رو اینجا بذار
TOKEN = 'توکن_ربات_تو_اینجا'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! خوش اومدی به ربات من 🤖")

# شروع ربات با polling
bot.infinity_polling()
