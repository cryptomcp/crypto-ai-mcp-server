"""Basic tests for the MCP Crypto Bot."""

import pytest
from src.config.env import get_settings


def test_settings_loading():
    """Test that settings can be loaded."""
    settings = get_settings()
    assert settings is not None
    assert isinstance(settings.live, bool)
    assert isinstance(settings.max_order_usd, float)


def test_safety_settings():
    """Test safety settings."""
    settings = get_settings()
    # In test mode, live trading should be disabled
    assert settings.live is False
    assert settings.am_i_sure == "NO"
