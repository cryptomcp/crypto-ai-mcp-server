# MCP Crypto Bot (Python)

[![MCP](https://img.shields.io/badge/MCP-Compliant-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMiA3VjE3TDEyIDIyTDIyIDE3VjdMMTIgMloiIHN0cm9rZT0iY3VycmVudENvbG9yIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNMTIgMjJWMTRMMiA5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTIyIDlMMTIgMTRMMiA5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+)](https://modelcontextprotocol.io)

Production-ready Model Context Protocol (MCP) server for crypto trading automation with AI decision support.

## 🚀 Features

### Core Functionality
- **Multi-Exchange Support**: CEX (Binance, etc.), EVM chains, Solana
- **AI Decision Engine**: OpenAI GPT-4, Google Gemini, DeepSeek integration
- **Telegram Bot**: Real-time management and notifications
- **Risk Management**: Configurable limits and safety checks
- **Wallet Management**: EVM and Solana wallet creation/import/export
- **Portfolio Tracking**: Real-time balance and position monitoring

### Trading Features
- **CEX Trading**: Spot orders, OHLCV data, balance management
- **DEX Integration**: 0x swaps on EVM, Jupiter swaps on Solana
- **Token Transfers**: ERC20 and SPL token transfers
- **AI Trading Assistant**: Intelligent trade recommendations with risk assessment
- **News Trading**: Real-time news monitoring, sentiment analysis, and AI-powered trading decisions

## 📋 Requirements

- Python 3.11+
- Linux/macOS/Windows
- API keys for exchanges and AI providers

## 🛠️ Installation

### Option 1: One-liner Installation (Recommended)

```bash
# Install with pipx (isolated environment)
pipx install mcp-crypto-bot

# Or with uv (fast package manager)
uvx install mcp-crypto-bot

# Run from anywhere
mcp-crypto-bot
```

### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/cryptomcp/crypto-ai-mcp-server.git
cd crypto-ai-mcp-server

# Install in development mode
pip install -e .

# Or using uv (recommended)
uv pip install -e .
```

### Environment Configuration
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

## 🚀 Usage

### Quick Start

```bash
# Start the MCP server
mcp-crypto-bot

# Or with custom environment
TELEGRAM_BOT_TOKEN=your_token mcp-crypto-bot
```

### MCP Inspector Integration

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run with Inspector
npx @modelcontextprotocol/inspector -- mcp-crypto-bot

# With environment injection
npx @modelcontextprotocol/inspector --env-file .env -- mcp-crypto-bot
```

## 🛠️ MCP Tools & Resources

### Available Tools
- **CEX Trading**: Price checks, order placement, balance management
- **EVM Operations**: Token transfers, DEX swaps, NFT operations
- **Solana Support**: SPL token transfers, Jupiter swaps, wallet management
- **AI Decision Engine**: Intelligent trading recommendations
- **Portfolio Management**: Balance tracking and portfolio snapshots
- **News Trading**: News monitoring, sentiment analysis, trending analysis, custom conditions

### Available Resources
- **`resource: wallets`**: List current EVM and Solana wallets
- **`resource: candles://{venue}/{symbol}/{timeframe}`**: Real-time OHLCV data

### News Trading Features
- **Real-time News Monitoring**: RSS feeds, APIs, web scraping from multiple sources
- **Sentiment Analysis**: AI-powered sentiment analysis with OpenAI, Gemini, and TextBlob
- **Custom Trading Conditions**: Rule-based trading with sentiment, frequency, keyword, and trending conditions
- **Trending Analysis**: Multi-platform trending coin detection and ranking
- **AI Decision Making**: Intelligent trading decisions based on news and market data
- **Risk Management**: Position sizing, stop-loss, take-profit, and daily limits
- **Trading Modes**: Manual, AI-assisted, and fully automated trading

### Example Usage

```python
from mcp import ClientSession

async with ClientSession() as session:
    # Get wallet information
    wallets = await session.read_resource("resource: wallets")
    
    # Get market data
    candles = await session.read_resource("resource: candles://binance/BTC/USDT/1h")
    
    # Execute trading operations
    result = await session.call_tool("cex_get_price", {"symbol": "BTC/USDT"})
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LIVE` | Enable live trading (0=test, 1=live) | Yes | `0` |
| `AM_I_SURE` | Safety confirmation for live trading | Yes | `NO` |
| `MAX_ORDER_USD` | Maximum order size in USD | Yes | `100` |
| `DAILY_LOSS_LIMIT_USD` | Daily loss limit in USD | Yes | `200` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No | - |
| `OWNER_TELEGRAM_ID` | Your Telegram user ID | No | - |
| `OPENAI_API_KEY` | OpenAI API key for AI decisions | No | - |
| `GOOGLE_API_KEY` | Google AI API key | No | - |
| `DEEPSEEK_API_KEY` | DeepSeek API key | No | - |
| `BINANCE_API_KEY` | Binance API key | No | - |
| `BINANCE_SECRET` | Binance secret key | No | - |
| `ETHEREUM_RPC_URL` | Ethereum RPC endpoint | No | - |
| `SOLANA_RPC_URL` | Solana RPC endpoint | No | - |

### Safety Configuration

```bash
# Test mode (safe)
LIVE=0
AM_I_SURE=NO
MAX_ORDER_USD=100
DAILY_LOSS_LIMIT_USD=200

# Live trading (dangerous - only if you know what you're doing)
LIVE=1
AM_I_SURE=YES
MAX_ORDER_USD=1000
DAILY_LOSS_LIMIT_USD=1000
```

## 📚 Documentation

View the full documentation at **[docs.cryptomcp.github.io](https://cryptomcp.github.io/crypto-ai-mcp-server/)**

### 🏃‍♂️ Running Documentation Locally

```bash
# 1. Navigate to docs directory
cd docs

# 2. Install dependencies
npm install

# 3. Start development server
npm run start

# 4. Open browser to http://localhost:3000
```

### 🏗️ Building Documentation

```bash
# Build for production
npm run build

# Serve built documentation locally
npm run serve
```

### 🚀 Deploying to GitHub Pages

```bash
# Deploy to GitHub Pages
npm run deploy

# Documentation will be available at:
# https://cryptomcp.github.io/crypto-ai-mcp-server/
```

## ⚠️ Risk Management

### Safety Features
- **Double Confirmation**: `LIVE=1` AND `AM_I_SURE=YES` required
- **Order Limits**: `MAX_ORDER_USD` enforces maximum trade size
- **Loss Limits**: `DAILY_LOSS_LIMIT_USD` prevents excessive losses
- **Dry Run Mode**: Test all operations with `dry_run: true`
- **Risk Assessment**: AI evaluates all trade recommendations

### Critical Safety Rules
1. **Never** set `LIVE=1` without `AM_I_SURE=YES`
2. **Always** test with `dry_run: true` first
3. **Monitor** daily loss limits
4. **Backup** wallet private keys securely
5. **Start Small**: Begin with small amounts

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
pytest tests/ -m integration
```

### Manual Testing
```bash
# Start server in test mode
LIVE=0 python src/server.py

# Use MCP inspector
npx @modelcontextprotocol/inspector -- python src/server.py
```

## 🏗️ Architecture

```
src/
├── server.py              # MCP server bootstrap
├── mcp_tools.py           # All MCP tool definitions
├── config/
│   └── env.py            # Environment configuration
├── cex/
│   └── ccxt_client.py    # CEX trading client
├── evm/
│   └── evm_client.py     # EVM blockchain client
├── solana/
│   └── solana_client.py  # Solana blockchain client
├── wallets/              # Wallet management
├── portfolio/            # Portfolio tracking
├── ai/                   # AI decision engine
│   ├── engine.py
│   └── prompts.py
├── telegram/
│   └── bot.py           # Telegram bot
└── logging.py           # Logging configuration
```

## 🔧 Development

### Adding New Tools
1. Define Pydantic model in `mcp_tools.py`
2. Implement tool function with `@mcp.tool()` decorator
3. Add error handling and logging
4. Update tests

### Adding New AI Providers
1. Add provider to `AIProvider` enum
2. Implement query method in `AIDecisionEngine`
3. Add to ensemble logic if desired
4. Update configuration

## 📝 API Reference

### Response Format
All tools return structured JSON:
```json
{
  "success": true|false,
  "data": { ... } | null,
  "error": "error message" | null
}
```

### Error Handling
- Network errors are automatically retried
- Validation errors return descriptive messages
- Risk violations prevent execution
- All errors are logged with context

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 24/7 Live Support

We provide **24/7 live support** with guaranteed **instant response** to all requests.  
- All requests are acknowledged within **5 minutes**.  
- Support is available **7 days a week, 24 hours a day** without interruption.  
- Resolution time may vary depending on the type of issue, but initial response is always instant.  
- We provide **multilingual support**, but our **primary language is English**.  

### Contact Us
- **Telegram** — [t.me/solbotsupport](https://t.me/solbotsupport)  
- **Email** — [info@solanatrade.bot](mailto:info@solanatrade.bot)  

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**This software is for educational and research purposes only. Crypto trading involves substantial risk of loss and is not suitable for every investor. Past performance does not guarantee future results. You should not trade with money you cannot afford to lose.**

**The authors and contributors of this project are not responsible for any financial losses incurred through the use of this software.**
