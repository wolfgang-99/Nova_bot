import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
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


# ------------------------------ flask ---------------------------------------------------------------
@app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    app.run(host='0.0.0.0', port=8080)


# ----------------------------- TELEGRAM BOT SECTION ----------------------------------------------------

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
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                [InlineKeyboardButton("Close", callback_data='button11')]
                ]
    return welcome_msg, InlineKeyboardMarkup(keyboard)


def get_buy_menu() -> tuple[str, InlineKeyboardMarkup]:
    buy_msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return buy_msg, InlineKeyboardMarkup(keyboard)


def get_positions_menu() -> tuple[str, InlineKeyboardMarkup]:
    postion_msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return postion_msg, InlineKeyboardMarkup(keyboard)


def get_wallet_menu() -> tuple[str, InlineKeyboardMarkup]:
    """Return formatted wallet menu message and keyboard"""
    msg = """
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
    return msg, InlineKeyboardMarkup(keyboard)


def get_sniper_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_orders_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_copy_trade_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_afk_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_auto_trade_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_nova_click_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_referrals_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_settings_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    """

    keyboard = [[InlineKeyboardButton("Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("Refresh", callback_data='Refresh')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


# ---------- COMMAND HANDLERS --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    msg, markup = get_main_menu()
    await update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML")


# ---------- CALLBACK HANDLERS -------------------
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return to main menu"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()
    msg, markup = get_main_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle buy button (button1)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_buy_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def positions_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle position button (button2)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_positions_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def wallet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet button (button3)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_wallet_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def sniper_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sniper button (button4)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_sniper_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def orders_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle orders button (button5)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_orders_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def copy_trade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle copy_trade button (button6)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_copy_trade_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def afk_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle afk button (button7)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_afk_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def auto_trade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle auto_trade button (button8)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_auto_trade_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def nova_click_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle nova_click button (button9)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_nova_click_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def referrals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle referrals button (button10)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_referrals_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle settings button (button11)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_settings_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML")


async def close_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle close button"""
    query = update.callback_query
    await query.answer()
    await query.message.delete()


# ----------------------- APPLICATION SETUP -------------------------------------------------------------
# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(buy_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(positions_callback, pattern="^button1$"))
    application.add_handler(CallbackQueryHandler(wallet_callback, pattern="^button2$"))
    application.add_handler(CallbackQueryHandler(wallet_callback, pattern="^button3$"))
    application.add_handler(CallbackQueryHandler(sniper_callback, pattern="^button4$"))
    application.add_handler(CallbackQueryHandler(orders_callback, pattern="^button5$"))
    application.add_handler(CallbackQueryHandler(copy_trade_callback, pattern="^button6$"))
    application.add_handler(CallbackQueryHandler(afk_callback, pattern="^button7$"))
    application.add_handler(CallbackQueryHandler(auto_trade_callback, pattern="^button8$"))
    application.add_handler(CallbackQueryHandler(nova_click_callback, pattern="^button9$"))
    application.add_handler(CallbackQueryHandler(referrals_callback, pattern="^button10$"))
    application.add_handler(CallbackQueryHandler(settings_callback, pattern="^button11$"))
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
