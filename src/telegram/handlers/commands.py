from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from src.telegram.filters import allowed_user_filter

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data['is_active'] = True
    await update.message.reply_text('Willkommen bei meinem Bot!')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data['is_active'] = False
    await update.message.reply_text('Bot wird gestoppt.')

start_handler = CommandHandler(
    command='start', 
    callback=start,
    filters=allowed_user_filter
)

stop_handler = CommandHandler(
    command='stop', 
    callback=stop,
    filters=allowed_user_filter
)