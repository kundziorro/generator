
from app import wallet


def test_get_value_in_pln():
    wallet_ = wallet.Wallet()
    result = wallet_.get_value_in_pln()

    assert result == 0