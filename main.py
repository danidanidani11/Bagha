import telebot, json, os, datetime, random
from flask import Flask, request
from telebot import types
from threading import Thread

API_TOKEN = '7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew'
bot.set_my_commands([
    telebot.types.BotCommand("start", "شروع ربات"),
])
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
    sample_questions = [

{
"question": "✈️ [مرحله 1] هواپیما سقوط کرده و شما در جنگلی تاریک هستید. اولین واکنش شما چیست؟",
"options": ["🏃 فرار می‌کنم", "🧭 نقشه می‌کشم", "🔥 آتش روشن می‌کنم", "😱 تسلیم می‌شوم"],
"answer": 2,
"explanations": {
0: "فرار بدون هدف ممکن است باعث گم‌شدگی بیشتر شود.",
1: "نقشه کشیدن بدون دید کافی بی‌فایده است.",
2: "✅ روشن کردن آتش باعث دیده شدن توسط تیم نجات می‌شود.",
3: "تسلیم شدن به معنای پایان تلاش برای بقا است."
}},

{
"question": "🌲 [مرحله 2] صدای شکست شاخه‌ای در پشت سرت می‌شنوی. چه می‌کنی؟",
"options": ["🔁 برمی‌گردم", "🏃 سریع دور می‌شوم", "🙈 پنهان می‌شوم", "📣 فریاد می‌زنم"],
"answer": 2,
"explanations": {
0: "برگشتن می‌تواند باعث رویارویی ناگهانی با خطر شود.",
1: "فرار صدای بیشتری تولید می‌کند.",
2: "✅ پنهان شدن در سکوت بهترین انتخاب برای حفظ جان است.",
3: "فریاد زدن خطر را به سمت شما می‌کشاند."
}},

{
"question": "🎒 [مرحله 3] به یک کوله‌پشتی می‌رسی. فقط یک آیتم جا دارد. کدام را برمی‌داری؟",
"options": ["💧 بطری آب", "🔪 چاقو", "🧭 قطب‌نما", "🍞 کنسرو غذا"],
"answer": 0,
"explanations": {
0: "✅ آب برای زنده ماندن از همه حیاتی‌تر است.",
1: "چاقو مهم است، اما بدون آب زنده نمی‌مانی.",
2: "قطب‌نما بدون مسیر مشخص کمک زیادی نمی‌کند.",
3: "غذا مهم است، اما بدن بدون آب سریع‌تر تحلیل می‌رود."
}},

{
"question": "🌌 [مرحله 4] شب است و باید پناهگاه پیدا کنی. کجا می‌خوابی؟",
"options": ["🌳 زیر درخت بزرگ", "🏔 کنار تخته‌سنگ", "💧 کنار نهر", "🏕 در فضای باز"],
"answer": 1,
"explanations": {
0: "زیر درخت خطر ریزش شاخه و حیوانات دارد.",
1: "✅ کنار تخته‌سنگ باد را می‌گیرد و محافظ نسبی است.",
2: "کنار نهر شب‌هنگام خطرناک است (مار، سرما).",
3: "خوابیدن در فضای باز خطر حمله حیوانات را دارد."
}},

{
"question": "🔥 [مرحله 5] چطور آتش درست می‌کنی؟",
"options": ["🪓 با زدن سنگ به چاقو", "📱 با لنز گوشی", "🧻 با مالش چوب‌ها", "💨 اصلاً آتش نمی‌زنم"],
"answer": 2,
"explanations": {
0: "سنگ به چاقو جرقه ندارد.",
1: "لنز گوشی کافی نیست، مخصوصاً در شب.",
2: "✅ مالش چوب‌ها روش سنتی ولی مؤثر برای ایجاد آتش است.",
3: "نبود آتش مساوی است با سرما و خطر در شب."
}},

{
"question": "📡 [مرحله 6] صدای سیگنال رادیویی می‌شنوی. چه می‌کنی؟",
"options": ["🏃 دنبال صدا می‌رم", "📣 فریاد می‌زنم", "🔊 صبر می‌کنم تا واضح‌تر شود", "📻 سیگنال را نادیده می‌گیرم"],
"answer": 0,
"explanations": {
0: "✅ دنبال کردن صدا ممکن است به تجهیزات یا کمک برسد.",
1: "فریاد زدن باعث هدر رفتن انرژی و جلب حیوانات می‌شود.",
2: "صبر ممکن است فرصت را از بین ببرد.",
3: "نادیده گرفتن سیگنال، از دست دادن راه نجات است."
}},

{
"question": "🕳 [مرحله 7] غاری پیدا می‌کنی. وارد می‌شی؟",
"options": ["✅ آره، پناهگاه خوبیه", "نه، خطرناکه", "داخل صدا می‌زنم", "فقط نزدیک می‌مونم"],
"answer": 3,
"explanations": {
0: "ورود بدون بررسی خطرناک است.",
1: "فرصت پناه گرفتن را از دست می‌دهی.",
2: "صدا زدن می‌تواند حیوانات را تحریک کند.",
3: "✅ نزدیک ماندن ایمن‌تر است و امکان بررسی را فراهم می‌کند."
}},

{
"question": "🌧 [مرحله 8] باران شدید می‌بارد. بهترین انتخاب؟",
"options": ["🏃 راه بیفتم", "⛺ زیر درخت بایستم", "🪵 سرپناه بسازم", "🪑 بنشینم و صبر کنم"],
"answer": 2,
"explanations": {
0: "راه رفتن در باران خطر افتادن و گم‌شدن را افزایش می‌دهد.",
1: "زیر درخت خطرناک است.",
2: "✅ سرپناه باعث گرم‌ماندن و حفظ انرژی می‌شود.",
3: "نشستن در معرض باران باعث هیپوترمی می‌شود."
}},

{
"question": "🍄 [مرحله 9] قارچ ناشناخته پیدا می‌کنی. چکار می‌کنی؟",
"options": ["🍽 می‌خورم", "📷 عکس می‌گیرم", "🚫 رها می‌کنم", "👃 بو می‌کنم"],
"answer": 2,
"explanations": {
0: "خوردن قارچ ناشناس می‌تواند کشنده باشد.",
1: "عکس گرفتن مفید است اما فوری نیست.",
2: "✅ رها کردن امن‌ترین تصمیم است.",
3: "بو کردن قارچ هم می‌تواند باعث مسمومیت شود."
}},

{
"question": "🦴 [مرحله 10] جسد حیوانی می‌بینی. کنارش استخوان تازه است. چه می‌کنی؟",
"options": ["🔍 بررسی می‌کنم", "🚫 دور می‌شم", "📍 علامت‌گذاری می‌کنم", "📸 عکس می‌گیرم"],
"answer": 1,
"explanations": {
0: "بررسی ممکن است شما را درگیر بوی لاشه کند.",
1: "✅ دور شدن از محل احتمال مواجهه با شکارچی را کم می‌کند.",
2: "علامت‌گذاری زمان‌بر است و ارزش ندارد.",
3: "عکس گرفتن کار بی‌فایده‌ای در بقاست."
}},

{
"question": "🧭 [مرحله 11] قطب‌نمایی پیدا می‌کنی، ولی نقشه نداری. چکار می‌کنی؟",
"options": ["🧭 کورکورانه به شمال می‌رم", "📍 دنبال مسیر پاکوب می‌گردم", "🚶 هر سمتی که راحت‌تره می‌رم", "🏕 صبر می‌کنم"],
"answer": 1,
"explanations": {
0: "حرکت کورکورانه در جنگل می‌تونه باعث گم‌شدگی بیشتر بشه.",
1: "✅ دنبال کردن مسیر پاکوب احتمال رسیدن به کمک رو بالا می‌بره.",
2: "راحت‌ترین مسیر ممکنه به مرداب یا خطر منتهی بشه.",
3: "صبر ممکنه فرصت نجات رو ازت بگیره."
}},

{
"question": "🔊 [مرحله 12] صدای جیغ انسانی می‌شنوی. واکنش؟",
"options": ["🏃 به سمت صدا", "📣 جواب می‌دی", "🚫 نادیده می‌گیری", "🔭 با دقت گوش می‌دی"],
"answer": 3,
"explanations": {
0: "حرکت سریع بدون اطلاع از وضعیت ممکنه خطرناک باشه.",
1: "فریاد زدن توجه حیوانات رو هم جلب می‌کنه.",
2: "نادیده گرفتن ممکنه کمک به انسانی نیازمند رو از بین ببره.",
3: "✅ گوش دادن و ارزیابی صدا قبل از هر واکنشی هوشمندانه‌تره."
}},

{
"question": "📻 [مرحله 13] رادیویی پیدا می‌کنی، ولی خراب شده. چکار می‌کنی؟",
"options": ["🔋 باطری‌هاشو برمی‌داری", "🛠 سعی می‌کنی تعمیرش کنی", "📦 رهاش می‌کنی", "📡 به عنوان سیگنال‌ساز استفاده می‌کنی"],
"answer": 3,
"explanations": {
0: "باطری مفید هست ولی به تنهایی کمکی به ارسال کمک نمی‌کنه.",
1: "تعمیر بدون ابزار ممکن نیست.",
2: "دور انداختن ابزار الکترونیکی اشتباهه.",
3: "✅ استفاده از آنتن و قطعات برای سیگنال‌دهی هوشمندانه‌ست."
}},

{
"question": "🪓 [مرحله 14] یک تبر زنگ‌زده پیدا می‌کنی. استفاده؟",
"options": ["🪓 باهاش درخت می‌برم", "🧼 تمیزش می‌کنی", "💧 در آب می‌شوری", "🗑 دورش می‌اندازی"],
"answer": 1,
"explanations": {
0: "استفاده از ابزار زنگ‌زده خطر آسیب و عفونت داره.",
1: "✅ تمیز کردن ابزار اولویت داره قبل استفاده.",
2: "آب به تنهایی زنگ رو از بین نمی‌بره.",
3: "ابزار مفید هیچ‌وقت نباید دور انداخته بشه."
}},

{
"question": "🐍 [مرحله 15] با ماری مواجه می‌شی. چی‌کار می‌کنی؟",
"options": ["🗡 بهش حمله می‌کنی", "🚶 به‌آرومی دور می‌شی", "🧱 روش چیزی می‌اندازی", "📷 عکس می‌گیری"],
"answer": 1,
"explanations": {
0: "حمله، مار رو تحریک به نیش‌زدن می‌کنه.",
1: "✅ دور شدن آرام کمترین ریسک رو داره.",
2: "حرکت سریع باعث واکنش مار میشه.",
3: "گرفتن عکس یعنی بی‌توجهی به خطر."
}},

{
"question": "💧 [مرحله 16] آبی پیدا می‌کنی ولی بو می‌ده. واکنش؟",
"options": ["🚰 می‌خوری چون تشنه‌ای", "🔥 می‌جوشونی", "📦 رها می‌کنی", "🧪 بو می‌کنی و می‌نوشی"],
"answer": 1,
"explanations": {
0: "نوشیدن آب آلوده ممکنه باعث اسهال و مرگ بشه.",
1: "✅ جوشوندن آب تا حد زیادی اون رو ایمن می‌کنه.",
2: "دور انداختن بدون بررسی اشتباهه.",
3: "بو کردن نشون نمی‌ده که آب آلوده نیست."
}},

{
"question": "🕯 [مرحله 17] کبریت‌هاتو خیس کردی. چکار می‌کنی؟",
"options": ["🌞 تو آفتاب خشک می‌کنی", "🔥 با سنگ آتش درست می‌کنی", "📦 بی‌خیال می‌شی", "🧻 چوب مرطوب می‌سوزونی"],
"answer": 0,
"explanations": {
0: "✅ خشک کردن کبریت‌ها شاید بتونه دوباره بهت فرصت آتش بده.",
1: "سنگ زدن به چوب بدون آتش‌زنه مؤثر نیست.",
2: "کبریت هنوز می‌تونه مفید باشه؛ نباید بی‌خیالش شد.",
3: "چوب مرطوب نمی‌سوزه و فقط دود ایجاد می‌کنه."
}},

{
"question": "📦 [مرحله 18] جعبه کمک‌های اولیه داری. چه چیزی اول لازمه؟",
"options": ["🩹 چسب زخم", "💊 آنتی‌بیوتیک", "🧴 ضدعفونی‌کننده", "🩺 باند"],
"answer": 2,
"explanations": {
0: "چسب زخم بدون تمیزکردن زخم فایده نداره.",
1: "آنتی‌بیوتیک باید با احتیاط مصرف بشه.",
2: "✅ اول زخم باید تمیز بشه تا عفونت نکنه.",
3: "باند برای بعد از تمیزکردن زخم استفاده می‌شه."
}},

{
"question": "🌄 [مرحله 19] از تپه بلندی منظره‌ای وسیع می‌بینی. چی‌کار می‌کنی؟",
"options": ["📍 علامت می‌ذاری", "🔦 سیگنال می‌دی", "🎯 پایین می‌ری", "🚫 بی‌تفاوت رد می‌شی"],
"answer": 1,
"explanations": {
0: "علامت‌گذاری مفیده ولی اولویت نیست.",
1: "✅ موقعیت بالا بهترین فرصت برای سیگنال‌دادنه.",
2: "پایین رفتن شاید باعث گم شدن بشه.",
3: "بی‌توجهی به چنین موقعیتی اشتباه بزرگیه."
}},

{
"question": "🥫 [مرحله 20] کنسرو باز کردی اما بو می‌ده. می‌خوری؟",
"options": ["😷 نه، پرت می‌کنی", "🍽 یکم تست می‌کنی", "🔥 می‌پزی که بوش بره", "🚫 نگه می‌داری برای بعد"],
"answer": 0,
"explanations": {
0: "✅ کنسرو فاسد خیلی خطرناکه؛ نباید خورده بشه.",
1: "حتی یک قاشق هم ممکنه باعث مسمومیت شدید بشه.",
2: "پختن همه باکتری‌ها رو از بین نمی‌بره.",
3: "نگه‌داشتن غذای فاسد اشتباهه."
}},

{
"question": "⚠️ [مرحله 21] به شاخه‌ای برخورد می‌کنی که نشانه‌ای روش حک شده. چی‌کار می‌کنی؟",
"options": ["🔍 بررسی دقیق می‌کنی", "🚫 نادیده می‌گیری", "📸 عکس می‌گیری", "🧭 جهت حرکت رو عوض می‌کنی"],
"answer": 0,
"explanations": {
0: "✅ بررسی نشانه‌ها ممکنه اطلاعاتی از دیگر نجات‌یافته‌ها یا خطر بده.",
1: "نادیده گرفتن نشونه‌ها یعنی از فرصت آگاهی محروم می‌شی.",
2: "عکس بدون تحلیل کاربردی نداره در لحظه.",
3: "تغییر مسیر بدون دلیل ممکنه اشتباه باشه."
}},

{
"question": "🦅 [مرحله 22] پرنده‌ای عجیب با جیغ بلند بالا سرت پرواز می‌کنه. چه می‌کنی؟",
"options": ["🧭 دنبال مسیرش می‌ری", "📢 فریاد می‌زنی", "🔭 از دور نگاه می‌کنی", "🚶 از اون منطقه دور می‌شی"],
"answer": 2,
"explanations": {
0: "دنبال کردن حیوان بدون هدف ممکنه منتهی به خطر بشه.",
1: "فریاد زدن ممکنه توجه شکارچی‌ها رو جلب کنه.",
2: "✅ مشاهده از دور باعث حفظ امنیت و جمع‌آوری اطلاعات می‌شه.",
3: "دور شدن بدون ارزیابی موقعیت گاهی باعث از دست دادن شانس نجات می‌شه."
}},

{
"question": "🧊 [مرحله 23] شب دما به شدت پایین میاد. لباس خیس تنته. چه می‌کنی؟",
"options": ["🔥 آتیش درست می‌کنی", "🧥 لباس‌تو در میاری", "🏃 فعالیت می‌کنی", "🛌 می‌خوابی"],
"answer": 0,
"explanations": {
0: "✅ آتش باعث گرم شدن سریع و جلوگیری از هیپوترمی می‌شه.",
1: "لباس خیس اگر درآورده نشه، باعث افت دما می‌شه.",
2: "فعالیت در شب باعث خستگی و ریسک بیشتره.",
3: "خواب با لباس خیس بسیار خطرناکه."
}},

{
"question": "🎯 [مرحله 24] صدای تیر می‌شنوی. چکار می‌کنی؟",
"options": ["🏃 به سمتش می‌ری", "🧎 پنهان می‌شی", "📣 کمک می‌خوای", "🚫 بی‌تفاوت رد می‌شی"],
"answer": 1,
"explanations": {
0: "نزدیک شدن به صدای تیراندازی خطرناکه.",
1: "✅ پنهان شدن امن‌ترین واکنشه.",
2: "فریاد در شرایط ناشناخته عاقلانه نیست.",
3: "نادیده گرفتن صدا می‌تونه شانس نجات یا خطر رو ازت بگیره."
}},

{
"question": "🦷 [مرحله 25] دندون‌درد شدید گرفتی و دارو نداری. چکار می‌کنی؟",
"options": ["🍃 از گیاه استفاده می‌کنی", "💧 آب سرد می‌خوری", "💤 صبر می‌کنی تا خوب شه", "🥄 چیزی با دندون نمی‌جوی"],
"answer": 0,
"explanations": {
0: "✅ برخی گیاهان مثل میخک اثر تسکین دارند.",
1: "آب سرد درد رو بیشتر می‌کنه.",
2: "صبر کردن بدون اقدام نتیجه نداره.",
3: "نجویدن مؤثره اما موقته و درمان نیست."
}},

{
"question": "🚁 [مرحله 26] بالگرد امداد خیلی دور دیده می‌شه. چکار می‌کنی؟",
"options": ["📣 داد می‌زنی", "🔥 آتش بزرگ می‌زنی", "📱 پیام می‌فرستی", "🖐 دست تکون می‌دی"],
"answer": 1,
"explanations": {
0: "فریاد به گوش خلبان نمی‌رسه.",
1: "✅ دود غلیظ بهترین علامت برای بالگرده.",
2: "در جنگل سیگنال موبایل نیست.",
3: "دست تکون دادن در فاصله زیاد بی‌فایده‌ست."
}},

{
"question": "🧵 [مرحله 27] زخمی عمیق داری. چه چیزی اولویت داره؟",
"options": ["🧼 تمیز کردن", "🩹 بستن", "🧪 آنتی‌بیوتیک", "🧊 کمپرس"],
"answer": 0,
"explanations": {
0: "✅ ضدعفونی قبل از هر چیزی مانع عفونت می‌شه.",
1: "بستن زخم قبل تمیز کردن باعث حبس آلودگی می‌شه.",
2: "آنتی‌بیوتیک دیر اثر می‌کنه و همیشه در دسترس نیست.",
3: "کمپرس درد رو کم می‌کنه ولی درمان نیست."
}},

{
"question": "🔦 [مرحله 28] چراغ قوه‌ات ضعیف شده. باتری نداری. چکار می‌کنی؟",
"options": ["🌙 از نور ماه استفاده می‌کنی", "📦 خاموشش می‌کنی برای بعد", "💥 می‌زنی به سنگ", "🪔 آتش درست می‌کنی"],
"answer": 1,
"explanations": {
0: "نور ماه کافیه اما در شب کامل نیست.",
1: "✅ خاموش کردن باتری رو برای مواقع ضروری نگه می‌داره.",
2: "زدن چراغ قوه خرابش می‌کنه.",
3: "آتش خوبه ولی نیاز به زمان و انرژی داره."
}},

{
"question": "📅 [مرحله 29] چند روز گذشته و امید نجات کم شده. چه می‌کنی؟",
"options": ["💀 تسلیم می‌شی", "📜 برنامه‌ریزی می‌کنی", "🚶 به دل جنگل می‌زنی", "😴 فقط استراحت می‌کنی"],
"answer": 1,
"explanations": {
0: "تسلیم شدن یعنی پایان بازی.",
1: "✅ ادامه حیات نیاز به برنامه و اراده داره.",
2: "حرکت بی‌برنامه می‌تونه کشنده باشه.",
3: "استراحت مداوم باعث تحلیل انرژی می‌شه."
}},

{
"question": "🌅 [مرحله 30] صبح روز هفتم، صدای افراد نزدیک شنیده می‌شه. آخرین انتخاب تو؟",
"options": ["📢 داد می‌زنی", "📡 علامت می‌دی", "🔥 دود ایجاد می‌کنی", "🏃 با تمام نیرو به سمت صدا می‌ری"],
"answer": 2,
"explanations": {
0: "داد ممکنه شنیده نشه.",
1: "علامت دادن موثره اما ممکنه دیده نشه.",
2: "✅ دود قوی‌ترین علامت دیداریه.",
3: "دویدن بدون ارزیابی ممکنه به خطر برسی."
}},

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
    return str(m.chat.id) in users and users[str(m.chat.id)]["name"] != ""

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

    # عضویت اجباری
    if not check_membership(m.chat.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(btn)
        bot.send_message(m.chat.id, "🔒 برای استفاده از ربات، ابتدا در کانال عضو شوید و سپس دوباره /start را بفرستید:", reply_markup=markup)
        return

    # اگه کاربر جدید باشه
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

    # ✅ بررسی اینکه اسم وارد کرده یا نه
    if users[str(m.chat.id)]["name"] == "":
        bot.send_message(m.chat.id, "👋 لطفاً نام خود را وارد کنید:")
        bot.register_next_step_handler(m, get_name)
    else:
        bot.send_message(m.chat.id, "👋 خوش آمدید!", reply_markup=main_menu())
        
def get_name(m):
    if m.text.startswith("/"):
        bot.send_message(m.chat.id, "❗️نام نمی‌تواند با / شروع شود. لطفاً فقط نام خود را وارد کنید:")
        bot.register_next_step_handler(m, get_name)
        return
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

@bot.message_handler(func=lambda m: True)
def block_if_no_name(m):
    if not check_name(m):
        if m.text != "/start":
            bot.send_message(m.chat.id, "❗️ لطفاً ابتدا نام خود را وارد کنید. /start")
            
if __name__ == "__main__":
    Thread(target=run).start()
