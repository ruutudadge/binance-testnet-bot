#!/usr/bin/env python3
"""
basic_bot.py
A reusable BasicBot class wrapping Binance Client for Futures (USDT-M Testnet).
Provides simple methods: place_market_order, place_limit_order, place_stop_limit.
Includes input validation and structured logging via utils.setup_logger.
This class is safe to use with testnet when client is configured accordingly.
"""

import logging
from typing import Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from .utils import setup_logger, validate_symbol, get_client

logger = setup_logger("logs/basic_bot.log")

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret)
        if testnet:
            # Testnet base URL for USDT-M Futures (as required)
            try:
                self.client.API_URL = "https://testnet.binancefuture.com"
            except Exception as e:
                logger.exception("Failed to set testnet API URL: %s", e)
        logger.info("BasicBot initialized (testnet=%s)", testnet)

    def place_market_order(self, symbol: str, side: str, quantity: float, recvWindow: int = 5000):
        symbol = symbol.upper()
        side = side.upper()
        validate_symbol(symbol)
        if side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")
        try:
            logger.info("Placing MARKET order %s %s qty=%s", side, symbol, quantity)
            res = self.client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity, recvWindow=recvWindow)
            logger.info("Market order response: %s", res)
            return res
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.exception("Binance error placing market order: %s", e)
            raise

    def place_limit_order(self, symbol: str, side: str, price: float, quantity: float, timeInForce: str = "GTC"):
        symbol = symbol.upper()
        side = side.upper()
        validate_symbol(symbol)
        if side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")
        try:
            logger.info("Placing LIMIT order %s %s qty=%s price=%s", side, symbol, quantity, price)
            res = self.client.futures_create_order(symbol=symbol, side=side, type="LIMIT", timeInForce=timeInForce, price=str(price), quantity=quantity)
            logger.info("Limit order response: %s", res)
            return res
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.exception("Binance error placing limit order: %s", e)
            raise

    def place_stop_limit(self, symbol: str, side: str, stop_price: float, limit_price: float, quantity: float):
        symbol = symbol.upper()
        side = side.upper()
        validate_symbol(symbol)
        try:
            logger.info("Placing STOP-LIMIT order %s %s qty=%s stop=%s limit=%s", side, symbol, quantity, stop_price, limit_price)
            res = self.client.futures_create_order(symbol=symbol, side=side, type="STOP", stopPrice=str(stop_price), price=str(limit_price), timeInForce="GTC", quantity=quantity)
            logger.info("Stop-Limit response: %s", res)
            return res
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.exception("Binance error placing stop-limit: %s", e)
            raise

if __name__ == "__main__":
    import os
    ak = os.environ.get("BINANCE_API_KEY") or "demo_key"
    sk = os.environ.get("BINANCE_API_SECRET") or "demo_secret"
    bot = BasicBot(ak, sk, testnet=True)
    print("BasicBot ready (demo).")
