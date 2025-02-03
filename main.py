import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from flask import Flask
from threading import Thread

# Flask server for Render health checks
app = Flask(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("bot_token")

# Configuration
TOKEN = BOT_TOKEN  # Replace with your bot token
WEBHOOK_URL = "https://nova-bot-m18w.onrender.com"  # Replace with your HTTPS URL
PORT = 10000  # Port to listen on (typically 443, 80, 88, or 8443)


# --------- flask ----------------------
@app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    app.run(host='0.0.0.0', port=8080)


# ---------- TELEGRAM BOT SECTION -------------------------
# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    welcome_msg = """
🌠 Welcome to Nova!

🚀 The Fastest All-In-One Trading Platform.

💳 Your Solana Wallets:

None - 0 SOL ($0.00 USD)
• Import or create new wallet to begin.
📖<a href="https://docs.tradeonnova.io/">Guide</a>
🐦<a href="https://x.com/TradeonNova">Twitter</a>
👥<a href="https://t.me/NovaSupportAgent">Support Channel</a>
▶<a href="https://www.youtube.com/@TradeonNova">YouTube</a>

🤖 Backup Bots:

🇺🇸 <a href="https://t.me/TradeoNovaBot">US1</a>
🇺🇸 <a href="https://t.me/TradeoNovaBot">US2</a>
🇪🇺 <a href="https://t.me/TradeoNovaBot">EU1</a>

💡 Ready to start trading? Send a token address to get started.
"""

    # Create inline keyboard buttons
    keyboard = [[InlineKeyboardButton("Buy", callback_data='buy')],
                [InlineKeyboardButton("Enter Access Code", callback_data='button2')],
                [InlineKeyboardButton("Enter Access Code", callback_data='button2')],
                [InlineKeyboardButton("Enter Access Code", callback_data='button2')],
                [InlineKeyboardButton("Enter Access Code", callback_data='button2')],
                [InlineKeyboardButton("Enter Access Code", callback_data='button2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send initial greeting message with buttons
    await context.bot.send_message(chat_id, welcome_msg, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id if query.message else update.effective_chat.id

    if query.data == "button2":
        await context.bot.send_message(chat_id, "Please enter your access or referral code.")
        context.user_data["awaiting_code"] = True


async def handle_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_code"):
        chat_id = update.effective_chat.id
        access_code = update.message.text.strip()
        keyboard = [[InlineKeyboardButton("Continue", callback_data='button3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if access_code == "Bullish":
            confirmation_msg = """
🎉 Congratulations! Your access code has been successfully approved!

Welcome to Nova — the Fastest All-In-One Trading Platform. Effortlessly trade any token on Solana with complete control at your fingertips.

✅ Access Granted: Nova Phase 1

Don't forget to join our Support channel and explore the guide below for a smooth start:

👉 <a href="https://t.me/TradeonNova">Join Support</a>
👉 <a href="https://docs.tradeonnova.io/">Nova Guide</a>
👉 <a href="https://www.youtube.com/@TradeonNova">YouTube</a>

💡 Ready to begin? Press Continue below to start using Nova.
"""
            await context.bot.send_message(chat_id, confirmation_msg, parse_mode="HTML", reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id, "❌ Invalid access code. Please try again.")
            context.user_data["awaiting_code"] = True


# Main function to run the bot
def main():
    # Create Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_access_code))

    # Run webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    Thread(target=run_flask).start()
    main()
