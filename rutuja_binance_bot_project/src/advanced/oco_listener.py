"""
advanced/oco_listener.py
Websocket listener to watch orders and automatically cancel the OCO counterpart when one side fills.
This uses python-binance's websocket; example uses threading and user data stream.
Note: You must provide API key/secret and keep the listenKey alive (via keepalive endpoint).
"""

import time, threading, logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.streams import ThreadedWebsocketManager

from utils import setup_logger

logger = setup_logger("advanced_oco_listener.log")

def start_oco_listener(client: Client, symbol: str, tp_order_id: int, sl_order_id: int):
    """
    Start a websocket listener for order updates. When either tp or sl order is filled (status == 'FILLED' or 'CANCELED' by reduce), cancel the other.
    This is a lightweight implementation — for production use a resilient reconnection and listenKey keepalive is needed.
    """
    twm = ThreadedWebsocketManager(api_key=client.API_KEY, api_secret=client.API_SECRET)
    twm.start()
    def handle_message(msg):
        # msg is a dict; check for ORDER_TRADE_UPDATE or ORDER_UPDATE depending on stream
        try:
            logger.info("WS message: %s", msg)
            event_type = msg.get("e") or msg.get("eventType") or msg.get("e", "")
            # different websocket formats exist; normalize
            order = None
            if msg.get("e") == "ORDER_TRADE_UPDATE":
                order = msg.get("o", {})
            elif msg.get("e") == "ORDER_UPDATE":
                order = msg.get("o", {})
            elif "order" in msg:
                order = msg.get("order")
            if not order:
                return
            order_id = int(order.get("i") or order.get("orderId") or 0)
            status = order.get("X") or order.get("status")
            logger.info("Order update id=%s status=%s", order_id, status)
            if order_id == tp_order_id and status in ("FILLED", "CANCELED", "REJECTED"):
                # cancel SL
                try:
                    logger.info("TP filled/canceled — cancelling SL order %s", sl_order_id)
                    client.futures_cancel_order(symbol=symbol, orderId=sl_order_id)
                except BinanceAPIException as e:
                    logger.exception("Error cancelling SL: %s", e)
            if order_id == sl_order_id and status in ("FILLED", "CANCELED", "REJECTED"):
                # cancel TP
                try:
                    logger.info("SL filled/canceled — cancelling TP order %s", tp_order_id)
                    client.futures_cancel_order(symbol=symbol, orderId=tp_order_id)
                except BinanceAPIException as e:
                    logger.exception("Error cancelling TP: %s", e)
        except Exception as e:
            logger.exception("Error handling ws message: %s", e)

    # Subscribe to user data stream
    listen_key = client.futures_get_listen_key().get("listenKey")
    logger.info("Obtained listenKey: %s", listen_key)
    twm.start_user_socket(callback=handle_message)
    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Shutting down listener")
    finally:
        twm.stop()
