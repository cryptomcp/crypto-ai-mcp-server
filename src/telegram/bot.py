"""Telegram bot for crypto trading management."""

from typing import Dict, Any
from telegram import Bot
from telegram.ext import Application
from loguru import logger

from ..config.env import get_settings
from ..logging import get_logger

log = get_logger(__name__)
settings = get_settings()


class TelegramBot:
    """Telegram bot for crypto trading management."""
    
    def __init__(self):
        """Initialize the Telegram bot."""
        self.bot = None
        self.application = None
        self._initialize_bot()
    
    def _initialize_bot(self):
        """Initialize the Telegram bot."""
        if not settings.telegram_bot_token:
            log.warning("Telegram bot token not configured")
            return
        
        try:
            self.bot = Bot(token=settings.telegram_bot_token)
            self.application = Application.builder().token(settings.telegram_bot_token).build()
            log.info("Telegram bot initialized successfully")
        except Exception as e:
            log.error(f"Failed to initialize Telegram bot: {e}")
            self.bot = None
            self.application = None
    
    async def start(self):
        """Start the Telegram bot."""
        if not self.application:
            log.warning("Telegram bot not initialized")
            return
        
        try:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            log.info("Telegram bot started successfully")
        except Exception as e:
            log.error(f"Failed to start Telegram bot: {e}")
            raise
    
    async def stop(self):
        """Stop the Telegram bot."""
        if self.application:
            try:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                log.info("Telegram bot stopped successfully")
            except Exception as e:
                log.error(f"Failed to stop Telegram bot: {e}")
