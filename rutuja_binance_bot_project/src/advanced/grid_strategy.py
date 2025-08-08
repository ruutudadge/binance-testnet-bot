"""
advanced/grid_strategy.py
Grid trading strategy: places a series of limit buy and sell orders between a price range.
This is a basic example — production needs risk checks, position sizing, and concurrency safety.
"""

import logging, math
from utils import setup_logger, validate_symbol
from binance.exceptions import BinanceAPIException

logger = setup_logger("advanced_grid.log")

def create_grid(client, symbol: str, lower: float, upper: float, grid_size: int, quantity: float, test=False):
    validate_symbol(symbol)
    if lower >= upper:
        raise ValueError("lower must be less than upper")
    if grid_size < 2:
        raise ValueError("grid_size must be at least 2")
    step = (upper - lower) / (grid_size - 1)
    orders = []
    logger.info("Creating grid for %s between %s and %s steps=%s qty=%s", symbol, lower, upper, step, quantity)
    for i in range(grid_size):
        price = lower + step * i
        side = "BUY" if i < grid_size//2 else "SELL"
        try:
            logger.info("Placing %s at %s", side, price)
            res = client.futures_create_order(symbol=symbol, side=side, type="LIMIT", price=str(price), timeInForce="GTC", quantity=quantity) if not test else {"test":"grid_%d"%i, "price":price, "side":side}
            orders.append(res)
        except BinanceAPIException as e:
            logger.exception("Error placing grid order at %s: %s", price, e)
    logger.info("Grid created with %d orders", len(orders))
    return orders
