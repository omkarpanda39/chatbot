from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from tweet_generator import handle_telegram_message
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def start(update, context):
    await update.message.reply_text(
        "Send me a topic (and optionally an affiliate link) to generate a tweet thread!\nFormat: <topic> | <affiliate_link> (link optional)"
    )

async def handle_message(update, context):
    text = update.message.text.strip()
    if "|" in text:
        topic, affiliate_link = [part.strip() for part in text.split("|", 1)]
    else:
        topic = text
        affiliate_link = None
    thread = handle_telegram_message(topic, affiliate_link)
    await update.message.reply_text(thread)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()