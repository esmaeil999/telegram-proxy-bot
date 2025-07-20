import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# تنظیم لاگر برای دیباگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # توکن رو از متغیر محیطی بخون

scheduler = AsyncIOScheduler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Proxy bot is active and will send a new list every 4 hours."
    )

async def send_proxy_list():
    # کد ارسال لیست پراکسی به کاربران اینجا بنویس
    logger.info("Sending proxy list to users...")
    # مثلا میتونی پیام بفرستی به یک چت خاص یا همه اعضا

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # زمان‌بندی ارسال لیست پراکسی هر 4 ساعت
    scheduler.add_job(send_proxy_list, 'interval', hours=4)
    scheduler.start()

    logger.info("✅ Proxy Bot started. Waiting for commands...")

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
