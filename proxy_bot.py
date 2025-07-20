import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()

async def send_proxy_list():
    # اینجا کد ارسال لیست پراکسی رو بنویس
    print("Sending proxy list...")

async def start(update, context):
    await update.message.reply_text("✅ Proxy Bot is active and will send a new list every 4 hours.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    scheduler.add_job(send_proxy_list, 'interval', hours=4)
    scheduler.start()

    await app.run_polling()

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        asyncio.create_task(main())
    else:
        asyncio.run(main())
