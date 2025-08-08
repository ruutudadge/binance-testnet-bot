#!/usr/bin/env python3
"""
limit_orders.py
Place a limit order on Binance USDT-M Futures (CLI).
Usage:
    python src/limit_orders.py --symbol BTCUSDT --side SELL --price 40000 --quantity 0.001 --time-in-force GTC --api-key YOUR_KEY --api-secret YOUR_SECRET --test
"""

import argparse
import logging
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from utils import setup_logger, validate_symbol, get_client

logger = setup_logger("limit_orders.log")

def place_limit_order(client, symbol: str, side: str, price: float, quantity: float, tif="GTC", test: bool=False):
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    validate_symbol(symbol)
    try:
        logger.info("Placing limit order: %s %s %s @%s", side, quantity, symbol, price)
        res = client.futures_create_order(symbol=symbol, side=side, type="LIMIT", timeInForce=tif, quantity=quantity, price=str(price), reduceOnly=False, newOrderRespType="RESULT", recvWindow=5000)
        logger.info("Order response: %s", res)
        print("Order placed. Response:")
        print(res)
    except (BinanceAPIException, BinanceOrderException) as e:
        logger.exception("Binance exception when placing limit order: %s", e)
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
    parser.add_argument("--price", required=True, type=float)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--time-in-force", default="GTC")
    parser.add_argument("--api-key", required=False)
    parser.add_argument("--api-secret", required=False)
    parser.add_argument("--test", action="store_true", help="Use testnet or test flag")
    args = parser.parse_args()
    client = get_client(args.api_key, args.api_secret, test=args.test)
    place_limit_order(client, args.symbol, args.side, args.price, args.quantity, tif=args.time_in_force, test=args.test)

if __name__ == "__main__":
    main()
