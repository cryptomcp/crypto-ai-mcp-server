"""CCXT client for centralized exchange trading."""

import asyncio
from typing import Dict, Any, List, Optional
import ccxt.async_support as ccxt
from loguru import logger

from ..config.env import get_settings
from ..logging import get_logger

log = get_logger(__name__)
settings = get_settings()


class CCXTClient:
    """CCXT client for centralized exchange operations."""
    
    def __init__(self):
        """Initialize the CCXT client."""
        self.exchange = None
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """Initialize the exchange connection."""
        if not settings.binance_api_key:
            log.warning("Binance API key not configured")
            return
        
        try:
            self.exchange = ccxt.binance({
                'apiKey': settings.binance_api_key,
                'secret': settings.binance_secret,
                'sandbox': not settings.live,  # Use sandbox in test mode
                'enableRateLimit': True,
            })
            log.info("Binance exchange initialized successfully")
        except Exception as e:
            log.error(f"Failed to initialize Binance exchange: {e}")
            self.exchange = None
    
    async def test_connection(self) -> bool:
        """Test the connection to the exchange."""
        if not self.exchange:
            raise Exception("Exchange not initialized")
        
        try:
            await self.exchange.fetch_balance()
            log.info("Exchange connection test successful")
            return True
        except Exception as e:
            log.error(f"Exchange connection test failed: {e}")
            raise
    
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol."""
        if not self.exchange:
            raise Exception("Exchange not initialized")
        
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                "symbol": symbol,
                "price": ticker["last"],
                "bid": ticker["bid"],
                "ask": ticker["ask"],
                "volume": ticker["baseVolume"],
                "timestamp": ticker["timestamp"]
            }
        except Exception as e:
            log.error(f"Failed to get price for {symbol}: {e}")
            raise
    
    async def get_balance(self) -> Dict[str, Any]:
        """Get account balance."""
        if not self.exchange:
            raise Exception("Exchange not initialized")
        
        try:
            balance = await self.exchange.fetch_balance()
            # Filter out zero balances
            non_zero_balances = {
                currency: amount for currency, amount in balance["total"].items()
                if amount > 0
            }
            return {
                "balances": non_zero_balances,
                "total_usd": balance.get("USD", 0)
            }
        except Exception as e:
            log.error(f"Failed to get balance: {e}")
            raise
    
    async def get_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[List[float]]:
        """Get OHLCV data for a symbol."""
        if not self.exchange:
            raise Exception("Exchange not initialized")
        
        try:
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            log.error(f"Failed to get OHLCV for {symbol}: {e}")
            raise
    
    async def place_order(self, symbol: str, side: str, type: str, amount: float, price: Optional[float] = None, dry_run: bool = True) -> Dict[str, Any]:
        """Place an order on the exchange."""
        if not self.exchange:
            raise Exception("Exchange not initialized")
        
        if dry_run:
            log.info(f"DRY RUN: Would place {side} {amount} {symbol} at {price or 'market'}")
            return {
                "id": "dry_run_order",
                "symbol": symbol,
                "side": side,
                "type": type,
                "amount": amount,
                "price": price,
                "status": "dry_run",
                "message": "This was a dry run - no actual order was placed"
            }
        
        try:
            order = await self.exchange.create_order(symbol, type, side, amount, price)
            log.info(f"Order placed successfully: {order['id']}")
            return order
        except Exception as e:
            log.error(f"Failed to place order: {e}")
            raise
    
    async def close(self):
        """Close the exchange connection."""
        if self.exchange:
            await self.exchange.close()
            log.info("Exchange connection closed")
