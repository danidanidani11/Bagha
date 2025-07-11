import telebot

TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
bot = telebot.TeleBot(TOKEN)

# حذف webhook قبلی (برای جلوگیری از ارور 409)
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! خوش اومدی به ربات ماجراجویی بقا 🌲🔥")

bot.infinity_polling()
