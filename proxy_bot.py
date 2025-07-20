import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import os

TOKEN = os.getenv("BOT_TOKEN", "توکن_ربات_اینجا")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Proxy bot is active and will send a new list every 4 hours.")

async def send_proxy_list():
    try:
        response = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all")
        proxies = response.text.strip()
        if proxies:
            print("🔗 Sending proxy list...")
            # اینجا می‌تونی کد ارسال پروکسی‌ها به کاربر رو بذاری
        else:
            print("⚠️ No proxies found.")
    except Exception as e:
        print(f"❌ Error fetching proxies: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_proxy_list, 'interval', hours=4)
    scheduler.start()

    print("✅ Proxy Bot started. Waiting for commands...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
