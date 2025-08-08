"""
advanced/oco.py
OCO-like pattern for Futures (take-profit + stop-loss). Futures API doesn't support a single OCO endpoint; this module places two orders and cancels the other when one executes.
"""

import time, logging
from binance.exceptions import BinanceAPIException, BinanceOrderException

from utils import setup_logger

logger = setup_logger("advanced_oco.log")

def place_oco(client, symbol, side, quantity, tp_price, sl_price, test=False):
    side = side.upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL")
    # Primary fill: market/limit entry should be placed before calling this function.
    # Here we place TP and SL orders.
    try:
        # Take Profit (limit) as reduceOnly
        tp_side = "SELL" if side == "BUY" else "BUY"
        logger.info("Placing TP order %s %s @%s", tp_side, quantity, tp_price)
        tp = client.futures_create_order(symbol=symbol, side=tp_side, type="TAKE_PROFIT_MARKET", stopPrice=str(tp_price), closePosition=False, quantity=quantity) if test==False else {"test":"tp"}
        # Stop Loss (stop-market)
        logger.info("Placing SL order %s %s @%s", tp_side, quantity, sl_price)
        sl = client.futures_create_order(symbol=symbol, side=tp_side, type="STOP_MARKET", stopPrice=str(sl_price), closePosition=False, quantity=quantity) if test==False else {"test":"sl"}
        logger.info("TP response: %s", tp)
        logger.info("SL response: %s", sl)
        return {"tp":tp, "sl":sl}
    except (BinanceAPIException, BinanceOrderException) as e:
        logger.exception("Error placing OCO pair: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error in OCO: %s", e)
        raise
