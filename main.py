import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from db import MongoDB
from solana_utils import get_user_wallet_info
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize MongoDB
mongo_client = MongoDB(os.getenv('MONGO_URI'))

# Main function to start the bot
def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    # Register command handlers
    application.add_handler(CommandHandler('start', start))

    # Start polling
    application.run_polling()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command to initialize the bot and show main menu."""
    user_id = update.effective_user.id
    wallet_info = get_user_wallet_info(mongo_client, user_id)

    # Build the welcome message
    message = f"Welcome! Your unique wallet address: {wallet_info['address']}\nDate and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Create inline buttons
    keyboard = [
        [InlineKeyboardButton("💧 Refresh", callback_data='refresh')],
        [InlineKeyboardButton("📈 Copy Trading", callback_data='copy_trading')],
        [InlineKeyboardButton("📉 Trading", callback_data='trading')],
        [InlineKeyboardButton("💰 Deposit", callback_data='deposit')],
        [InlineKeyboardButton("🚪 Withdraw", callback_data='withdraw')],
        [InlineKeyboardButton("🎉 Invite", callback_data='invite')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Await the asynchronous methods
    await update.message.reply_photo(photo=open('img/mark.webp', 'rb'))  # Send image
    await update.message.reply_text(message, reply_markup=reply_markup)

if __name__ == '__main__':
    main()