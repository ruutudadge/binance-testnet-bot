#!/usr/bin/env python3
"""
market_orders.py
Place a market order on Binance USDT-M Futures (CLI).
Usage:
    python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --api-key YOUR_KEY --api-secret YOUR_SECRET --test
"""

import argparse
import logging
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from utils import setup_logger, validate_symbol, get_client

logger = setup_logger("market_orders.log")

def place_market_order(client, symbol: str, side: str, quantity: float, test: bool=False):
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    validate_symbol(symbol)
    try:
        if test:
            logger.info("Placing test market order: %s %s %s", side, quantity, symbol)
            res = client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity, newOrderRespType="RESULT", recvWindow=5000)
        else:
            logger.info("Placing market order: %s %s %s", side, quantity, symbol)
            res = client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity, newOrderRespType="RESULT", recvWindow=5000)
        logger.info("Order response: %s", res)
        print("Order placed. Response:")
        print(res)
    except (BinanceAPIException, BinanceOrderException) as e:
        logger.exception("Binance exception when placing market order: %s", e)
        print("Error placing order:", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print("Unexpected error:", e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--api-key", required=False)
    parser.add_argument("--api-secret", required=False)
    parser.add_argument("--test", action="store_true", help="Use testnet or test flag")
    args = parser.parse_args()
    client = get_client(args.api_key, args.api_secret, test=args.test)
    place_market_order(client, args.symbol, args.side, args.quantity, test=args.test)

if __name__ == "__main__":
    main()
