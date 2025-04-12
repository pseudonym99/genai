from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Willkommen bei meinem Bot!')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot wird gestoppt.')

start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)