"""Environment configuration management."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Risk Management (CRITICAL)
    live: bool = Field(default=False, description="Enable live trading (0=test, 1=live)")
    am_i_sure: str = Field(default="NO", description="Safety confirmation for live trading")
    max_order_usd: float = Field(default=100.0, description="Maximum order size in USD")
    daily_loss_limit_usd: float = Field(default=200.0, description="Daily loss limit in USD")
    
    # Telegram Bot
    telegram_bot_token: Optional[str] = Field(default=None, description="Telegram bot token")
    owner_telegram_id: Optional[int] = Field(default=None, description="Owner Telegram user ID")
    
    # AI Providers
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    google_api_key: Optional[str] = Field(default=None, description="Google AI API key")
    deepseek_api_key: Optional[str] = Field(default=None, description="DeepSeek API key")
    
    # CEX Configuration
    binance_api_key: Optional[str] = Field(default=None, description="Binance API key")
    binance_secret: Optional[str] = Field(default=None, description="Binance secret key")
    
    # Blockchain RPC
    ethereum_rpc_url: Optional[str] = Field(default=None, description="Ethereum RPC endpoint")
    solana_rpc_url: Optional[str] = Field(default="https://api.mainnet-beta.solana.com", description="Solana RPC endpoint")
    
    # EVM Configuration
    evm_private_key: Optional[str] = Field(default=None, description="EVM private key")
    solana_private_key: Optional[str] = Field(default=None, description="Solana private key")
    
    # API Keys
    zeroex_api_key: Optional[str] = Field(default=None, description="0x API key")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def can_execute_trade() -> bool:
    """Check if trading is allowed based on safety settings."""
    settings = get_settings()
    return settings.live and settings.am_i_sure == "YES"
