#!/usr/bin/env python3
"""
stop_limit_orders.py
Place a stop-limit order on Binance USDT-M Futures (CLI).
Usage:
    python src/stop_limit_orders.py --symbol BTCUSDT --side BUY --stop-price 30000 --limit-price 29900 --quantity 0.01 --api-key KEY --api-secret SECRET --test
"""

import argparse, sys
from binance.exceptions import BinanceAPIException, BinanceOrderException
from utils import setup_logger, validate_symbol, get_client

logger = setup_logger("logs/stop_limit_orders.log")

def place_stop_limit(client, symbol: str, side: str, stop_price: float, limit_price: float, quantity: float, test: bool=False):
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    validate_symbol(symbol)
    if side == "BUY" and limit_price >= stop_price:
        raise ValueError("For BUY stop-limit, limit_price should be less than stop_price (trigger).")
    if side == "SELL" and limit_price <= stop_price:
        raise ValueError("For SELL stop-limit, limit_price should be greater than stop_price (trigger).")
    try:
        logger.info("Placing stop-limit: %s %s qty=%s stop=%s limit=%s", side, symbol, quantity, stop_price, limit_price)
        res = client.futures_create_order(
            symbol=symbol, side=side, type="STOP", stopPrice=str(stop_price),
            price=str(limit_price), timeInForce="GTC", quantity=quantity, reduceOnly=False
        ) if not test else {"test":"stop_limit"}
        logger.info("Stop-Limit response: %s", res)
        print("Response:", res)
    except (BinanceAPIException, BinanceOrderException) as e:
        logger.exception("Binance exception when placing stop-limit order: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--stop-price", required=True, type=float)
    parser.add_argument("--limit-price", required=True, type=float)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--api-key", required=False)
    parser.add_argument("--api-secret", required=False)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    client = get_client(args.api_key, args.api_secret, test=args.test)
    place_stop_limit(client, args.symbol, args.side, args.stop_price, args.limit_price, args.quantity, test=args.test)

if __name__ == "__main__":
    main()
