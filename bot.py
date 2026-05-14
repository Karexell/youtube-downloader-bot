"""
YouTube Downloader Telegram Bot - Main Entry Point
"""
import logging
from telegram.ext import Application
from config import TELEGRAM_BOT_TOKEN
from handlers import get_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the bot"""
    
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Error: TELEGRAM_BOT_TOKEN not set in environment!")
        print("Please set your Telegram Bot Token in .env file")
        return
    
    logger.info("Starting YouTube Downloader Bot...")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    for handler in get_handlers():
        application.add_handler(handler)
    
    logger.info("Bot started successfully!")
    logger.info("Send /start to your bot on Telegram")
    
    application.run_polling(allowed_updates=['message', 'callback_query'])


if __name__ == "__main__":
    main()