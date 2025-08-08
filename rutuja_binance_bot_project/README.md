# Rutuja_Dadge - Binance Futures Order Bot

## Overview
This project provides a CLI-based trading bot skeleton for Binance USDT-M Futures supporting Market and Limit orders, and offering advanced strategies like OCO (take-profit + stop-loss pair) and TWAP (time-weighted average price). It includes input validation, structured logging, and example usage.

> **Warning:** Trading on live futures markets carries financial risk. Use testnet and paper trading before using real funds.

## Requirements
- Python 3.9+
- Install dependencies:
```bash
pip install python-binance reportlab
```

## Project Structure
```
[project_root]/
├─ src/
│  ├─ market_orders.py
│  ├─ limit_orders.py
│  ├─ utils.py
│  └─ advanced/
│     ├─ oco.py
│     └─ twap.py
├─ bot.log
├─ report.pdf
└─ README.md
```

## Setup (Testnet)
1. Create API key & secret for Binance Futures Testnet: https://testnet.binancefuture.com/
2. Export keys:
```bash
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
```
3. Use `--test` flag to point the client to testnet (see utils.get_client).

## Usage examples
Market order (testnet):
```bash
python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --test --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET
```

Limit order:
```bash
python src/limit_orders.py --symbol BTCUSDT --side SELL --price 40000 --quantity 0.001 --time-in-force GTC --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET
```

TWAP example (from Python):
```python
from src.advanced.twap import execute_twap
# configure client as in utils.get_client and call execute_twap(client, "BTCUSDT", "BUY", total_qty=0.01, slices=5, interval_seconds=10, test=True)
```

OCO (conceptual):
- Futures API does not provide true OCO. The `advanced/oco.py` module places TP and SL orders and you must implement a listener (websocket or polling) to cancel the counterpart when one fills.

## Logging
All modules use structured logging (timestamp, level). Example logs are in `bot.log`.

## Notes & Next steps
- Add websocket order-trade listener to detect fills and cancel OCO counterpart.
- Implement Grid strategy and integrate Fear & Greed Index for sizing (bonus).
- Add unit tests and CI workflow for safety.


## Added Features
- JSON structured logging
- OCO websocket listener: `src/advanced/oco_listener.py`
- Grid strategy: `src/advanced/grid_strategy.py`

## Examples
Start OCO listener (after placing TP and SL):
```python
from src.advanced.oco_listener import start_oco_listener
# after placing tp and sl and obtaining their orderIds
start_oco_listener(client, "BTCUSDT", tp_order_id=123456, sl_order_id=123457)
```

Create a basic grid:
```python
from src.advanced.grid_strategy import create_grid
create_grid(client, "BTCUSDT", lower=30000, upper=40000, grid_size=11, quantity=0.001, test=True)
```


## Additional Files
- `stop_limit_orders.py` - CLI for stop-limit orders
- `.gitignore`, `requirements.txt`
- `tests/` - pytest unit tests
- `.github/workflows/ci.yml` - CI running pytest

## How to run tests
```bash
pip install -r requirements.txt
pytest -q
```

## GitHub setup (commands you should run locally)
```bash
# Create a private repo and push
git init
git add .
git commit -m "Initial commit - Binance Futures Bot"
# Create repo on GitHub (replace YOUR_USERNAME and REPO_NAME)
# Using gh (GitHub CLI):
gh repo create YOUR_USERNAME/dadge-rutuja-maroti-binance-bot --private --description "Binance Futures Order Bot" --confirm
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/dadge-rutuja-maroti-binance-bot.git
git push -u origin main
# Add collaborator (instructor)
# gh api or use web UI. Example with gh:
gh api --method PUT /repos/YOUR_USERNAME/dadge-rutuja-maroti-binance-bot/collaborators/INSTRUCTOR_USERNAME -f permission=push
```


## GitHub push commands (replace placeholders)
```bash
# After reviewing the project locally:
git init
git add .
git commit -m "Initial commit - Binance Futures Bot"
# Create private repo (using your GitHub username: ruutudadge)
# Using GitHub CLI:
gh repo create ruutudadge/dadge-rutuja-maroti-binance-bot --private --description "Binance Futures Order Bot" --confirm
git branch -M main
git remote add origin git@github.com:ruutudadge/dadge-rutuja-maroti-binance-bot.git
git push -u origin main
# Add instructor as collaborator (replace INSTRUCTOR_USERNAME):
gh api --method PUT /repos/ruutudadge/dadge-rutuja-maroti-binance-bot/collaborators/INSTRUCTOR_USERNAME -f permission=push
```


## BasicBot class
A reusable `BasicBot` is provided at `src/basic_bot.py` that wraps `python-binance.Client` and implements:
- `place_market_order(symbol, side, quantity)`
- `place_limit_order(symbol, side, price, quantity)`
- `place_stop_limit(symbol, side, stop_price, limit_price, quantity)`

Example usage:
```python
from src.basic_bot import BasicBot
import os
bot = BasicBot(os.environ.get('BINANCE_API_KEY'), os.environ.get('BINANCE_API_SECRET'), testnet=True)
res = bot.place_market_order('BTCUSDT', 'BUY', 0.001)
print(res)
```
