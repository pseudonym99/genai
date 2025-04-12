import logging
from telegram.ext import Application

from src.telegram.settings import TELEGRAM_SETTINGS
from src.telegram import commands, messages

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def main():
    application = Application.builder().token(
        TELEGRAM_SETTINGS.api_key.get_secret_value()
    ).build()
    
    # Füge Handler hinzu
    application.add_handler(commands.start_handler)
    application.add_handler(commands.stop_handler)
    application.add_handler(messages.text_handler)

    # Starte den Bot
    application.run_polling()

if __name__ == '__main__':
    main()