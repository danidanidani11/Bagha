import telebot

bot = telebot.TeleBot("7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew")  # 👈 توکن اصلیت
bot.remove_webhook()

print("✅ Webhook قبلی حذف شد.")
