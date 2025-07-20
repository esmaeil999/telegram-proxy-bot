import requests
import pytz
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "8105480654:AAGLPeftu12D6nimY1k8oEJYHHJ7Gj1XdZY"
CHAT_ID = 7463676240

PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=IR&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
]

async def get_proxies():
    proxies = []
    for url in PROXY_SOURCES:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies += response.text.strip().splitlines()
        except Exception as e:
            print(f"❌ Error fetching proxies from {url}: {e}")
    return list(set(proxies))

async def send_proxy_list(bot: Bot):
    proxies = await get_proxies()
    if proxies:
        proxy_text = "\n".join(proxies[:20])
        with open("proxies.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        await bot.send_message(chat_id=CHAT_ID, text=f"🔹 New Iranian proxy list:\n\n{proxy_text}")
        await bot.send_document(chat_id=CHAT_ID, document="proxies.txt")
    else:
        await bot.send_message(chat_id=CHAT_ID, text="❌ Could not fetch any proxies!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "✅ Proxy bot is active and will send a new list every 4 hours."
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    scheduler.add_job(send_proxy_list, 'interval', hours=4, args=[app.bot])
    scheduler.start()

    print("✅ Bot started and waiting for commands...")
    app.run_polling()

if name == "main":
    main()
