import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load Telegram bot token from environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

admin_user_id = "8096817817"  # Admin's user ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    # Send a greeting message to the user
    await update.message.reply_text(f"Hello! I am high-speed-trading bot. \n Your Telegram user Id is {user_id}.")

    # Send the user's ID to the admin
    await context.bot.send_message(chat_id=admin_user_id, text=f"New user started the bot: {user_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Help command!')

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()

if __name__ == '__main__':
    main()