import os
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from pymongo import MongoClient

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')  # Get MongoDB URI from environment variables.
DATABASE_NAME = os.getenv('DATABASE_NAME')  # Get MongoDB URI from environment variables.

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]  # Replace with your actual database name
wallets_collection = db['wallets']  # Replace with your actual collection name

async def start(query, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = query.from_user.id  
    wallet_info = wallets_collection.find_one({"user_id": user_id})

    # Get current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if wallet_info is None:
        new_wallet_address = generate_wallet_address() 

        wallets_collection.insert_one({
            "user_id": user_id,
            "wallet_address": new_wallet_address,
            "balance": 0,
            "usd_value": 0
        })
        wallet_info = {
            "wallet_address": new_wallet_address,
            "balance": 0,
            "usd_value": 0
        }

    message = (
        f"🕒 Current Time: {current_time}\n"
        f"💳 Wallet Address: {wallet_info['wallet_address']}\n"
        f"💰 Bitcoin Balance: {wallet_info['balance']} BTC\n"
        f"💵 Total USD Value: {wallet_info['usd_value']} USDT\n\n"
        "Check your cryptocurrency information here!"
    )

    buttons = [
        [InlineKeyboardButton("🔄 Refresh", callback_data='refresh'),
         InlineKeyboardButton("❌ Close", callback_data='close')]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.message.reply_text(message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'refresh':
        await start(update, context)  # Refresh wallet information
    elif query.data == 'close':
        await query.edit_message_text(text="❌ Session has ended. Thank you!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This bot helps you manage cryptocurrency wallets. Press 'Menu' for more options.")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu_text = (
        "📋 Menu:\n"
        "/start - View wallet information\n"
        "/help - Get help information\n"
        "/wallets - Manage wallets"
    )
    await update.message.reply_text(menu_text)

def generate_wallet_address():
    # Implement logic to generate a new wallet address. Replace the return statement with actual logic.
    return "new_wallet_address_here"

def generate_api_key_secret():
    # Implement logic to generate an API key secret. Replace the return statement with actual logic.
    return "generated_secret_here"

def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()