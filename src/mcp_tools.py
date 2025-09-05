"""MCP Tools definitions for the Crypto Bot."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger

from .config.env import get_settings, can_execute_trade
from .logging import get_logger

log = get_logger(__name__)
settings = get_settings()

# Base response model
class MCPResponse(BaseModel):
    """Standard MCP response format."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Basic tools for testing
async def get_status() -> Dict[str, Any]:
    """Get the current status of the MCP Crypto Bot."""
    return {
        "success": True,
        "data": {
            "status": "running",
            "version": "1.0.0",
            "environment": "LIVE" if settings.live else "TEST",
            "trading_enabled": can_execute_trade(),
            "features": {
                "cex_trading": bool(settings.binance_api_key),
                "evm_support": bool(settings.ethereum_rpc_url),
                "solana_support": bool(settings.solana_rpc_url),
                "ai_engine": bool(settings.openai_api_key or settings.google_api_key),
                "telegram_bot": bool(settings.telegram_bot_token),
                "news_trading": True
            }
        }
    }

async def get_config() -> Dict[str, Any]:
    """Get current configuration (without sensitive data)."""
    return {
        "success": True,
        "data": {
            "live_trading": settings.live,
            "safety_confirmed": settings.am_i_sure == "YES",
            "max_order_usd": settings.max_order_usd,
            "daily_loss_limit_usd": settings.daily_loss_limit_usd,
            "log_level": settings.log_level,
            "features_configured": {
                "binance": bool(settings.binance_api_key),
                "ethereum": bool(settings.ethereum_rpc_url),
                "solana": bool(settings.solana_rpc_url),
                "openai": bool(settings.openai_api_key),
                "google_ai": bool(settings.google_api_key),
                "telegram": bool(settings.telegram_bot_token)
            }
        }
    }

async def test_connection() -> Dict[str, Any]:
    """Test connections to various services."""
    results = {}
    
    # Test Binance connection
    if settings.binance_api_key:
        try:
            from .cex.ccxt_client import CCXTClient
            client = CCXTClient()
            await client.test_connection()
            results["binance"] = {"status": "connected", "error": None}
        except Exception as e:
            results["binance"] = {"status": "failed", "error": str(e)}
    else:
        results["binance"] = {"status": "not_configured", "error": None}
    
    # Test Ethereum connection
    if settings.ethereum_rpc_url:
        try:
            from .evm.evm_client import EVMClient
            client = EVMClient()
            await client.test_connection()
            results["ethereum"] = {"status": "connected", "error": None}
        except Exception as e:
            results["ethereum"] = {"status": "failed", "error": str(e)}
    else:
        results["ethereum"] = {"status": "not_configured", "error": None}
    
    # Test Solana connection
    if settings.solana_rpc_url:
        try:
            from .solana.solana_client import SolanaClient
            client = SolanaClient()
            await client.test_connection()
            results["solana"] = {"status": "connected", "error": None}
        except Exception as e:
            results["solana"] = {"status": "failed", "error": str(e)}
    else:
        results["solana"] = {"status": "not_configured", "error": None}
    
    return {
        "success": True,
        "data": results
    }

# Export tools for FastMCP
tools = {
    "get_status": get_status,
    "get_config": get_config,
    "test_connection": test_connection,
}