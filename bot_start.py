import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Changed variable name

# Import the start function from main
from main import start

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Path to the image. Set it to the correct absolute or relative path.
    image_path = 'img/mark.webp'  # Replace with the actual path to your image file

    # Send the image
    await update.message.reply_photo(photo=open(image_path, 'rb'))

    # Set up keyboard buttons
    keyboard = [
        [InlineKeyboardButton("🔄 Start", callback_data='start'),
         InlineKeyboardButton("🆘 Help", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Centered message structure
    message = (
        "🌟 What can this bot do? 🌟\n\n"
        "✨ This bot helps you copy trade Solana at high speed. ✨"
    )
    
    # Send the text message
    await update.message.reply_text(message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Add your help information here.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'start':
        # Call the start function with query instead of update
        await start(query, context)  # Pass query instead of update
    elif query.data == 'help':
        await help_command(query, context)


def main() -> None:
    # Create an Application object
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()  # Updated variable name

    # Register handlers
    app.add_handler(CommandHandler('start', command_start))  # Changed this
    app.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()