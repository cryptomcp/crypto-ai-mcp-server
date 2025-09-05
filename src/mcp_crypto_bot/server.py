#!/usr/bin/env python3
"""
MCP Crypto Bot Server - Main entry point for the MCP server.
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from typing import List, Dict, Any

from fastmcp import FastMCP
from loguru import logger

from ..config.env import get_settings
from ..logging import get_logger
from . import __version__

log = get_logger(__name__)
settings = get_settings()

# Create FastMCP app instance
app = FastMCP("mcp-crypto-bot")

# Add lifespan handler
@asynccontextmanager
async def lifespan(app):
    """Application lifespan manager."""
    log.info("Starting MCP Crypto Bot server...")
    
    # Initialize Telegram bot if configured
    if settings.telegram_bot_token:
        try:
            from ..telegram.bot import TelegramBot
            telegram_bot = TelegramBot()
            await telegram_bot.start()
            log.info("Telegram bot started successfully")
        except Exception as e:
            log.error(f"Failed to start Telegram bot: {e}")
    
    yield
    
    # Cleanup
    log.info("Shutting down MCP Crypto Bot server...")

app.lifespan = lifespan

# Add resources
@app.resource("wallets://")
async def list_wallets() -> List[Dict[str, Any]]:
    """List all available wallets (EVM and Solana)."""
    wallets = []
    
    try:
        # Get EVM wallets
        from ..wallets.evm_wallets import EVMWalletManager
        evm_manager = EVMWalletManager()
        evm_wallets = await evm_manager.list_wallets()
        for wallet in evm_wallets:
            wallets.append({
                "id": wallet["id"],
                "chain": "evm",
                "address": wallet["address"],
                "balance": wallet.get("balance", "0")
            })
    except Exception as e:
        log.error(f"Failed to list EVM wallets: {e}")
    
    try:
        # Get Solana wallets
        from ..wallets.sol_wallets import SolWalletManager
        sol_manager = SolWalletManager()
        sol_wallets = await sol_manager.list_wallets()
        for wallet in sol_wallets:
            wallets.append({
                "id": wallet["id"],
                "chain": "solana",
                "address": wallet["address"],
                "balance": wallet.get("balance", "0")
            })
    except Exception as e:
        log.error(f"Failed to list Solana wallets: {e}")
    
    return wallets

@app.resource("candles://{venue}/{symbol}/{timeframe}")
async def ohlcv_resource(venue: str, symbol: str, timeframe: str) -> List[Dict[str, Any]]:
    """Get OHLCV data for a specific venue, symbol, and timeframe."""
    try:
        from ..cex.ccxt_client import CCXTClient
        client = CCXTClient()
        
        # Get OHLCV data
        ohlcv_data = await client.get_ohlcv(symbol, timeframe, limit=100)
        
        # Convert to resource format
        candles = []
        for candle in ohlcv_data:
            candles.append({
                "timestamp": candle[0],
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })
        
        return candles
    except Exception as e:
        log.error(f"Failed to get OHLCV data for {venue}/{symbol}/{timeframe}: {e}")
        return []

# Register all existing tools from mcp_tools
from ..mcp_tools import tools
for tool_name, tool_func in tools.items():
    app.tool(tool_name)(tool_func)

async def main():
    """Main entry point for the MCP server."""
    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    log.info("Starting MCP Crypto Bot server...")
    log.info(f"Server version: {__version__}")
    log.info(f"Environment: {'LIVE' if settings.live else 'TEST'}")
    
    # Run the FastMCP app
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())