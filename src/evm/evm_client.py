"""EVM blockchain client for Ethereum and compatible chains."""

from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
from loguru import logger

from ..config.env import get_settings
from ..logging import get_logger

log = get_logger(__name__)
settings = get_settings()


class EVMClient:
    """EVM blockchain client for Ethereum operations."""
    
    def __init__(self):
        """Initialize the EVM client."""
        self.w3 = None
        self.account = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize the Web3 connection."""
        if not settings.ethereum_rpc_url:
            log.warning("Ethereum RPC URL not configured")
            return
        
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.ethereum_rpc_url))
            if self.w3.is_connected():
                log.info("Ethereum connection established")
            else:
                log.error("Failed to connect to Ethereum")
                self.w3 = None
        except Exception as e:
            log.error(f"Failed to initialize Ethereum connection: {e}")
            self.w3 = None
        
        # Initialize account if private key is provided
        if settings.evm_private_key:
            try:
                self.account = Account.from_key(settings.evm_private_key)
                log.info(f"EVM account initialized: {self.account.address}")
            except Exception as e:
                log.error(f"Failed to initialize EVM account: {e}")
                self.account = None
    
    async def test_connection(self) -> bool:
        """Test the connection to the EVM network."""
        if not self.w3:
            raise Exception("EVM client not initialized")
        
        try:
            # Test connection by getting latest block
            latest_block = self.w3.eth.get_block('latest')
            log.info(f"EVM connection test successful - Latest block: {latest_block.number}")
            return True
        except Exception as e:
            log.error(f"EVM connection test failed: {e}")
            raise
    
    async def get_eth_balance(self, address: str) -> Dict[str, Any]:
        """Get ETH balance for an address."""
        if not self.w3:
            raise Exception("EVM client not initialized")
        
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return {
                "address": address,
                "balance_wei": str(balance_wei),
                "balance_eth": float(balance_eth),
                "currency": "ETH"
            }
        except Exception as e:
            log.error(f"Failed to get ETH balance for {address}: {e}")
            raise
