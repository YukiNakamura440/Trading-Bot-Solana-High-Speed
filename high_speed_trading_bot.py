import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from auth import register_user, authenticate_user, check_user_exists  # Importing from auth.py

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Login", callback_data='login')],
        [InlineKeyboardButton("Register", callback_data='register')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! Please choose one of the options below:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'login':
        await query.edit_message_text("Please enter your email for login:")
        context.user_data['step'] = 3  # Set step for login process
    elif query.data == 'register':
        await query.edit_message_text("Please enter your email for registration:")
        context.user_data['step'] = 1  # Set step for registration process

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get('step')

    if step == 1:  # Getting email for registration
        email = update.message.text
        if check_user_exists(email):  # Check if the user already exists
            await update.message.reply_text("This email is already registered. Please log in or choose a different email.")
            del context.user_data['step']
        else:
            context.user_data['email'] = email
            await update.message.reply_text("Please enter your password:")
            context.user_data['step'] = 2
    elif step == 2:  # Getting password and registering user
        context.user_data['password'] = update.message.text
        registered = register_user(update.effective_user.id, 
                                   context.user_data['email'], 
                                   context.user_data['password'])
        if registered:
            await update.message.reply_text("Registration successful! You can now log in. Type /login to proceed.")
        else:
            await update.message.reply_text("Registration failed: invalid data. Please try again.")
        del context.user_data['step']  # Clear step after registration
    elif step == 3:  # Getting email for login
        context.user_data['email'] = update.message.text
        await update.message.reply_text("Please enter your password for authentication:")
        context.user_data['step'] = 4
    elif step == 4:  # Authenticating user
        user = authenticate_user(context.user_data['email'], update.message.text)
        if user:
            keyboard = [
                [InlineKeyboardButton("Next", callback_data='next')],
                [InlineKeyboardButton("Exit", callback_data='exit')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Welcome to the high-speed trading bot!", reply_markup=reply_markup)
            del context.user_data['step']  # Clear step after successful login
        else:
            await update.message.reply_text("Incorrect email or password. Please try again.")
            del context.user_data['step']  # Clear step on failure

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()