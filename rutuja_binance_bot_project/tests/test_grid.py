from src.advanced.grid_strategy import create_grid
class DummyClient:
    def futures_create_order(self, **kwargs):
        return {"ok": True, "kwargs": kwargs}
def test_grid_params():
    client = DummyClient()
    orders = create_grid(client, "BTCUSDT", lower=30000, upper=31000, grid_size=3, quantity=0.001, test=True)
    assert len(orders) == 3
