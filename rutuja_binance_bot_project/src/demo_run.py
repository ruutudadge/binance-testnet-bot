#!/usr/bin/env python3
"""
demo_run.py
Simulated end-to-end demo that uses a DummyClient to mimic Binance Futures responses.
Generates structured logs and screenshots (saved to demo_outputs/) to include in report.pdf.
This script does NOT call the real Binance API and is safe to run locally.
"""

import json, os, time
from src.utils import setup_logger
from PIL import Image, ImageDraw, ImageFont

logger = setup_logger("logs/demo_run.log")

class DummyClient:
    def futures_create_order(self, **kwargs):
        # Simulate an order response
        resp = {
            "orderId": int(time.time()*1000) % 1000000,
            "symbol": kwargs.get("symbol"),
            "side": kwargs.get("side"),
            "type": kwargs.get("type"),
            "price": kwargs.get("price"),
            "quantity": kwargs.get("quantity"),
            "status": "NEW"
        }
        logger.info("Mock order placed: %s", json.dumps(resp))
        return resp

def make_screenshot(text, path):
    # Simple image with text
    img = Image.new("RGB", (1000, 300), color=(255,255,255))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans.ttf", 14)
    except:
        f = ImageFont.load_default()
    y = 10
    for line in text.splitlines():
        d.text((10, y), line, fill=(0,0,0), font=f)
        y += 18
    img.save(path)

def run_demo():
    os.makedirs("demo_outputs", exist_ok=True)
    client = DummyClient()
    # Market order
    m = client.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001)
    make_screenshot("Market Order Response:\\n" + json.dumps(m, indent=2), "demo_outputs/market_order.png")
    time.sleep(0.2)
    # Limit order
    l = client.futures_create_order(symbol="BTCUSDT", side="SELL", type="LIMIT", price="40000", quantity=0.001)
    make_screenshot("Limit Order Response:\\n" + json.dumps(l, indent=2), "demo_outputs/limit_order.png")
    time.sleep(0.2)
    # Stop-limit (simulated)
    s = client.futures_create_order(symbol="BTCUSDT", side="BUY", type="STOP", stopPrice="30000", price="29950", quantity=0.001)
    make_screenshot("Stop-Limit Order Response:\\n" + json.dumps(s, indent=2), "demo_outputs/stop_limit.png")
    time.sleep(0.2)
    # TWAP slices
    slices = []
    for i in range(3):
        t = client.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.0003)
        slices.append(t)
    make_screenshot("TWAP slices responses:\\n" + json.dumps(slices, indent=2), "demo_outputs/twap.png")
    # Grid sample
    grid = []
    for p in [39000, 39500, 40000]:
        g = client.futures_create_order(symbol="BTCUSDT", side="BUY", type="LIMIT", price=str(p), quantity=0.0005)
        grid.append(g)
    make_screenshot("Grid orders responses:\\n" + json.dumps(grid, indent=2), "demo_outputs/grid.png")
    print("Demo complete. Outputs in demo_outputs/ and logs in logs/demo_run.log")

if __name__ == "__main__":
    run_demo()
