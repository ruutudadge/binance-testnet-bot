from src.advanced.twap import execute_twap
class DummyClient:
    def futures_create_order(self, **kwargs):
        return {"ok": True, "kwargs": kwargs}

def test_twap_slices(tmp_path):
    client = DummyClient()
    res = execute_twap(client, "BTCUSDT", "BUY", total_qty=0.01, slices=5, interval_seconds=0, test=True)
    assert len(res) == 5
