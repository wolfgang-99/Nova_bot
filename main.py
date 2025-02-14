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



# ---------- HELPER FUNCTIONS --------------------
def get_main_menu() -> tuple[str, InlineKeyboardMarkup]:
    """Return formatted main menu message and keyboard"""
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
    keyboard = [[InlineKeyboardButton("Buy", callback_data='button1'),
                 InlineKeyboardButton("Positions", callback_data='button2')],
                [InlineKeyboardButton("Wallets", callback_data='button3'),
                 InlineKeyboardButton("sniper", callback_data='button4')],
                [InlineKeyboardButton("Limit Orders", callback_data='button5'),
                 InlineKeyboardButton("Copy Trade", callback_data='button6')],
                [InlineKeyboardButton("AFK", callback_data='button7'),
                 InlineKeyboardButton("Auto Buy", callback_data='button8')],
                [InlineKeyboardButton("Nova Click", callback_data='button9'),
                 InlineKeyboardButton("Referrals", callback_data='button10')],
                [InlineKeyboardButton("Settings", callback_data='button11'),
                 InlineKeyboardButton("Refresh", callback_data='button12')],
                [InlineKeyboardButton("Close", callback_data='button11')]
                ]
    return welcome_msg, InlineKeyboardMarkup(keyboard)


def get_wallet_menu() -> tuple[str, InlineKeyboardMarkup]:
    """Return formatted wallet menu message and keyboard"""
    wallet_msg = """
            💳 Wallet Settings

            📚 Need more help? Click Here!

            🌐 Create, manage and import wallets here.

            💳 Your Solana Wallets:

            None - 0 SOL ($0.00 USD)
            • Import new wallet to begin.

            🔒 Tip: Keep your Nova wallets secure by setting a Security Pin below.

            💡 Select an option below.
                    """
    # Create inline keyboard buttons
    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='button2')],
                [InlineKeyboardButton("Change Default Wallet", callback_data='button3')],
                [InlineKeyboardButton(text="Create Wallet", callback_data="button4"),
                 InlineKeyboardButton(text="Import Wallet", callback_data="button5")],
                [InlineKeyboardButton(text="Rename Wallet", callback_data='button6'),
                 InlineKeyboardButton(text="Delete Wallet", callback_data='button7')],
                [InlineKeyboardButton(text="Withdraw", callback_data='button8'),
                 InlineKeyboardButton(text="EXPORT Private Key", callback_data='button9')],
                [InlineKeyboardButton(text="Security Pin Setup", callback_data='button10'),
                 InlineKeyboardButton(text="Settings", callback_data='button11')],
                ]
    return wallet_msg, InlineKeyboardMarkup(keyboard)


# ---------- COMMAND HANDLERS --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    msg, markup = get_main_menu()
    await update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")


# ---------- CALLBACK HANDLERS -------------------
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return to main menu"""
    query = update.callback_query # Acknowledge the button press
    await query.answer()
    msg, markup = get_main_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def wallet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet button (button3)"""
    query = update.callback_query # Acknowledge the button press
    await query.answer()

    msg, markup = get_wallet_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def close_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle close button"""
    query = update.callback_query
    await query.answer()
    await query.message.delete()


# ---------- APPLICATION SETUP -------------------
# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(wallet_callback, pattern="^button3$"))
    application.add_handler(CallbackQueryHandler(close_callback, pattern="^close$"))

    # Keep existing webhook setup
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    Thread(target=run_flask).start()
    main()
