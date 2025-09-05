"""EVM wallet management."""

from typing import Dict, Any, List
from eth_account import Account
from loguru import logger

from ..logging import get_logger

log = get_logger(__name__)


class EVMWalletManager:
    """EVM wallet management."""
    
    def __init__(self):
        """Initialize the EVM wallet manager."""
        self.wallets = []
    
    async def create_wallet(self) -> Dict[str, Any]:
        """Create a new EVM wallet."""
        try:
            account = Account.create()
            wallet = {
                "id": f"evm_{len(self.wallets) + 1}",
                "address": account.address,
                "private_key": account.key.hex(),
                "chain": "evm"
            }
            self.wallets.append(wallet)
            log.info(f"Created EVM wallet: {account.address}")
            return wallet
        except Exception as e:
            log.error(f"Failed to create EVM wallet: {e}")
            raise
    
    async def list_wallets(self) -> List[Dict[str, Any]]:
        """List all EVM wallets."""
        return self.wallets
