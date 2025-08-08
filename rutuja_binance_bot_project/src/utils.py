"""
utils.py
Shared utilities: JSON logger setup with rotation, client factory, and validations.
"""

import logging, os, sys, json
from logging import Logger
from logging.handlers import RotatingFileHandler
from binance.client import Client

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def setup_logger(filename: str = "logs/bot.log") -> Logger:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = RotatingFileHandler(filename, maxBytes=5*1024*1024, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(JsonFormatter())
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(JsonFormatter())
        logger.addHandler(sh)
    return logger

def validate_symbol(symbol: str):
    if not isinstance(symbol, str) or len(symbol) < 6 or not symbol.endswith("USDT"):
        raise ValueError("Symbol looks invalid. Example valid symbol: BTCUSDT")

def get_client(api_key: str = None, api_secret: str = None, test: bool=False):
    """
    Returns a configured Client. If api_key/secret are None, it will expect environment variables BINANCE_API_KEY and BINANCE_API_SECRET.
    For test=True you should configure the client to point at Binance futures testnet (see README).
    """
    ak = api_key or os.environ.get("BINANCE_API_KEY")
    sk = api_secret or os.environ.get("BINANCE_API_SECRET")
    if not ak or not sk:
        raise EnvironmentError("API key and secret must be provided either via args or environment variables.")
    client = Client(ak, sk)
    if test:
        # To use testnet, users should configure the base URL as described in the README.
        client.API_URL = "https://testnet.binancefuture.com"
    return client
