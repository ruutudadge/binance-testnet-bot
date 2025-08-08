from src.utils import validate_symbol
import pytest

def test_validate_symbol_ok():
    validate_symbol("BTCUSDT")

def test_validate_symbol_fail():
    with pytest.raises(ValueError):
        validate_symbol("BTC")
