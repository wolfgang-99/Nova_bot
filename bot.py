import os
import logging
from flask import Flask, request
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("bot_token")

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot application
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Webhook URL (Replace YOUR_RENDER_URL with actual Render URL)
WEBHOOK_URL = f"https://nova-bot-0rvq.onrender.com/webhook"

# Enable logging
logging.basicConfig(level=logging.INFO)

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    welcome_msg = """
🌠 Welcome to Nova!
The fastest Telegram Bot on Solana.
Nova allows you to buy or sell tokens in lightning fast speed and also has many features including:
Migration Sniping, Copy-trading, Limit Orders & a lot more.

💡 Have an access code?
• Enter it below to unlock instant access.

⏳ No access code?
• Tap the button below to join the queue and be the first to experience lightning-fast transactions.

🚀 Let's get started!
"""

    keyboard = [
        [InlineKeyboardButton("Join Queue", callback_data='button1')],
        [InlineKeyboardButton("Enter Access Code", callback_data='button2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id, welcome_msg, reply_markup=reply_markup)

# Callback for button presses
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id if query.message else update.effective_chat.id

    if query.data == "button2":
        await context.bot.send_message(chat_id, "Please enter your access or referral code.")
        context.user_data["awaiting_code"] = True

# Handle user access code input
async def handle_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_code"):
        chat_id = update.effective_chat.id
        access_code = update.message.text.strip()

        if access_code == "Bullish":
            confirmation_msg = """
🎉 Congratulations! Your access code has been successfully approved!

Welcome to Nova — the Fastest All-In-One Trading Platform. Effortlessly trade any token on Solana with complete control at your fingertips.

✅ Access Granted: Nova Phase 1

Don't forget to join our Support channel and explore the guide below for a smooth start:

👉 [Join Support](https://t.me/TradeonNova)
👉 Nova Guide
👉 YouTube

💡 Ready to begin? Press Continue below to start using Nova.
"""
            await context.bot.send_message(chat_id, confirmation_msg, parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id, "❌ Invalid access code. Please try again.")

        context.user_data["awaiting_code"] = False

# Flask route to handle Telegram webhook updates
@app.route('/')
def home():
    return "Bot is running!"


@app.route('/webhook', methods=['POST'])
async def webhook():
    print("Webhook called")
    update = Update.de_json(request.get_json(force=True), bot_app.bot)

    # ✅ Explicitly initialize the bot
    if not bot_app.running:
        await bot_app.initialize()

    # ✅ Run process_update as an async task
    await bot_app.process_update(update)

    return "OK", 200


# Function to set the Telegram webhook
async def set_webhook():
    bot = bot_app.bot  # ✅ FIXED: No need to await in v21+
    await bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    # Start Flask app
    app.run(debug=True, port=443)
