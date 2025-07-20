import requests
import pytz
import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("BOT_TOKEN")  # توکن باید توی Environment Variable به اسم BOT_TOKEN ذخیره شده باشه
CHAT_ID = int(os.getenv("CHAT_ID", "7463676240"))  # آیدی چت هم بهتره محیطی باشه

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
            print(f"⚠️ Error fetching proxies from {url}: {e}")
    return list(set(proxies))

async def send_proxy_list(bot: Bot):
    proxies = await get_proxies()
    if proxies:
        proxy_text = "\n".join(proxies[:20])
        with open("proxies.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        await bot.send_message(chat_id=CHAT_ID, text=f"🔗 New Iranian proxy list:\n\n{proxy_text}")
        await bot.send_document(chat_id=CHAT_ID, document="proxies.txt")
    else:
        await bot.send_message(chat_id=CHAT_ID, text="⚠️ Could not fetch any proxies!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "✅ Proxy bot is active and will send a new list every 4 hours."
    await update.message.reply_text(text)

async def scheduled_job(app):
    await send_proxy_list(app.bot)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler(timezone=pytz.utc)
    # اجرای تابع async در scheduler
    scheduler.add_job(lambda: asyncio.create_task(scheduled_job(app)), 'interval', hours=4)
    scheduler.start()

    print("✅ Bot started and waiting for commands...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
