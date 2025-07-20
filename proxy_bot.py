import requests
import pytz
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "8105480654:AAGLPeftu12D6nimY1k8oEJYHHJ7Gj1XdZY"
CHAT_ID = 7463676240

DEFAULT_INTERVAL_HOURS = 4
DEFAULT_LANGUAGE = "en"
DEFAULT_COUNTRY = "ir"

# Proxy sources for IR and ALL
PROXY_SOURCES_IR = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=IR&ssl=all&anonymity=all",
]
PROXY_SOURCES_ALL = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

user_settings = {
    "interval": DEFAULT_INTERVAL_HOURS,
    "language": DEFAULT_LANGUAGE,
    "country": DEFAULT_COUNTRY
}

def get_message(key: str):
    messages = {
        "en": {
            "start": "? Proxy bot is active and will send a new list every {} hours.",
            "proxies_sent": "?? New proxy list sent!",
            "error_fetch": "? Could not fetch any proxies!",
            "interval_changed": "? Interval changed to {} hours.",
            "invalid_interval": "? Invalid interval. Please enter a number.",
            "country_changed": "? Country set to '{}'.",
            "lang_changed": "? Language changed to English.",
        },
        "fa": {
            "start": "? ???? ?????? ???? ?? ? ?? {} ???? ???? ????????.",
            "proxies_sent": "?? ???? ???? ?????? ????? ??!",
            "error_fetch": "? ???????? ???? ????????? ?? ?????? ???!",
            "interval_changed": "? ????? ????? ?? {} ???? ????? ???.",
            "invalid_interval": "? ????? ????? ??????? ???. ????? ?? ??? ???? ????.",
            "country_changed": "? ???? ?? '{}' ????? ????.",
            "lang_changed": "? ???? ?? ????? ????? ????.",
        }
    }
    return messages[user_settings["language"]][key]

async def get_proxies():
    sources = PROXY_SOURCES_IR if user_settings["country"] == "ir" else PROXY_SOURCES_ALL
    proxies = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies += response.text.strip().splitlines()
        except Exception as e:
            print(f"? Error fetching proxies from {url}: {e}")
    return list(set(proxies))

async def send_proxy_list(bot: Bot):
    proxies = await get_proxies()
    if proxies:
        proxy_text = "\n".join(proxies[:20])
        with open("proxies.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        await bot.send_message(chat_id=CHAT_ID, text=f"{get_message('proxies_sent')}\n\n{proxy_text}")
        await bot.send_document(chat_id=CHAT_ID, document="proxies.txt")
    else:
        await bot.send_message(chat_id=CHAT_ID, text=get_message("error_fetch"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_message("start").format(user_settings["interval"])
    await update.message.reply_text(text)

async def getproxies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_proxy_list(context.bot)

async def setinterval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hours = int(context.args[0])
        user_settings["interval"] = hours
        scheduler.reschedule_job("send_job", trigger='interval', hours=hours)
        await update.message.reply_text(get_message("interval_changed").format(hours))
    except:
        await update.message.reply_text(get_message("invalid_interval"))

async def setcountry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.args[0].lower()
    if country in ["ir", "all"]:
        user_settings["country"] = country
        await update.message.reply_text(get_message("country_changed").format(country))
    else:
        await update.message.reply_text("? Invalid country. Use 'ir' or 'all'.")

async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.args[0].lower()
    if lang in ["en", "fa"]:
        user_settings["language"] = lang
        await update.message.reply_text(get_message("lang_changed"))
    else:
        await update.message.reply_text("? Invalid language. Use 'en' or 'fa'.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getproxies", getproxies))
app.add_handler(CommandHandler("setinterval", setinterval))
app.add_handler(CommandHandler("setcountry", setcountry))
app.add_handler(CommandHandler("lang", setlang))

scheduler = AsyncIOScheduler(timezone=pytz.utc)
scheduler.add_job(send_proxy_list, 'interval', hours=user_settings["interval"], args=[app.bot], id="send_job")
scheduler.start()

print("? Bot started and waiting for commands...")
app.run_polling()