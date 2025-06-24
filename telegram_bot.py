import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from tweet_generator import handle_telegram_message

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Telegram Bot Handlers
async def start(update, context):
    await update.message.reply_text(
        "Send me a topic (and optionally an affiliate link) to generate a tweet thread!\n"
        "Format: <topic> | <affiliate_link> (link optional)"
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

# Function to run bot in a thread
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# Flask web server for Render port binding
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running on Render."

if __name__ == "__main__":
    # Start the Telegram bot in a background thread
    threading.Thread(target=run_bot).start()

    # Start dummy web server (Render requires this)
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)
