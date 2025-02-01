from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("bot_token")


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

    # Create inline keyboard buttons
    keyboard = [[InlineKeyboardButton("Join Queue", callback_data='button1')],
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
    bot_token = BOT_TOKEN

    # Create the bot application
    app = ApplicationBuilder().token(bot_token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_access_code))

    # Run the bot
    print("Bot is running...")
    app.run_polling()
