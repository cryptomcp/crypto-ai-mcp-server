"""Solana wallet management."""

from typing import Dict, Any, List
from solders.keypair import Keypair
from loguru import logger

from ..logging import get_logger

log = get_logger(__name__)


class SolWalletManager:
    """Solana wallet management."""
    
    def __init__(self):
        """Initialize the Solana wallet manager."""
        self.wallets = []
    
    async def create_wallet(self) -> Dict[str, Any]:
        """Create a new Solana wallet."""
        try:
            keypair = Keypair()
            wallet = {
                "id": f"sol_{len(self.wallets) + 1}",
                "address": str(keypair.pubkey()),
                "private_key": keypair.secret().hex(),
                "chain": "solana"
            }
            self.wallets.append(wallet)
            log.info(f"Created Solana wallet: {keypair.pubkey()}")
            return wallet
        except Exception as e:
            log.error(f"Failed to create Solana wallet: {e}")
            raise
    
    async def list_wallets(self) -> List[Dict[str, Any]]:
        """List all Solana wallets."""
        return self.wallets
