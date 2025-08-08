"""
advanced/twap.py
Simple TWAP: split a large order into n equal parts and place them at intervals.
"""

import time, logging
from utils import setup_logger, validate_symbol
from binance.exceptions import BinanceAPIException, BinanceOrderException

logger = setup_logger("advanced_twap.log")

def execute_twap(client, symbol, side, total_qty, slices=10, interval_seconds=30, test=False):
    validate_symbol(symbol)
    side = side.upper()
    qty_per_slice = float(total_qty) / int(slices)
    logger.info("Starting TWAP: %s %s total=%s slices=%s every=%ss", side, symbol, total_qty, slices, interval_seconds)
    results = []
    for i in range(int(slices)):
        try:
            logger.info("Placing slice %d: qty %s", i+1, qty_per_slice)
            res = client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=qty_per_slice) if not test else {"test":"twap_slice_%d"% (i+1)}
            results.append(res)
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.exception("Error on TWAP slice %d: %s", i+1, e)
        time.sleep(interval_seconds)
    logger.info("TWAP finished. Results count: %d", len(results))
    return results
