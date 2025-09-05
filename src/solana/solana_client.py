"""Solana blockchain client."""

from typing import Dict, Any, Optional
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey
from loguru import logger

from ..config.env import get_settings
from ..logging import get_logger

log = get_logger(__name__)
settings = get_settings()


class SolanaClient:
    """Solana blockchain client."""
    
    def __init__(self):
        """Initialize the Solana client."""
        self.client = None
        self.keypair = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize the Solana connection."""
        if not settings.solana_rpc_url:
            log.warning("Solana RPC URL not configured")
            return
        
        try:
            self.client = AsyncClient(settings.solana_rpc_url)
            log.info("Solana connection established")
        except Exception as e:
            log.error(f"Failed to initialize Solana connection: {e}")
            self.client = None
        
        # Initialize keypair if private key is provided
        if settings.solana_private_key:
            try:
                # Convert private key string to bytes and create keypair
                private_key_bytes = bytes.fromhex(settings.solana_private_key)
                self.keypair = Keypair.from_bytes(private_key_bytes)
                log.info(f"Solana keypair initialized: {self.keypair.pubkey()}")
            except Exception as e:
                log.error(f"Failed to initialize Solana keypair: {e}")
                self.keypair = None
    
    async def test_connection(self) -> bool:
        """Test the connection to the Solana network."""
        if not self.client:
            raise Exception("Solana client not initialized")
        
        try:
            # Test connection by getting latest block height
            block_height = await self.client.get_block_height()
            log.info(f"Solana connection test successful - Latest block: {block_height}")
            return True
        except Exception as e:
            log.error(f"Solana connection test failed: {e}")
            raise
    
    async def get_sol_balance(self, pubkey: str) -> Dict[str, Any]:
        """Get SOL balance for a public key."""
        if not self.client:
            raise Exception("Solana client not initialized")
        
        try:
            public_key = PublicKey.from_string(pubkey)
            balance = await self.client.get_balance(public_key)
            sol_balance = balance.value / 1e9  # Convert lamports to SOL
            return {
                "pubkey": pubkey,
                "balance_lamports": balance.value,
                "balance_sol": sol_balance,
                "currency": "SOL"
            }
        except Exception as e:
            log.error(f"Failed to get SOL balance for {pubkey}: {e}")
            raise
