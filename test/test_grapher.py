from app.wallet import Transaction
from app.visualization import Grapher
import pandas as pd


def test_create_historical_rates_df(mocker):
    mocker.patch(
        "app.requester.ExchangeRateRequester.get_historical_bids", return_value={"date": "2021-09-06", "rate": 4.2}
    )
    grapher = Grapher()
    transactions = Transaction("2021-09-06", 100, 4.2)
    result = grapher._create_historical_rates_df(transactions)
    df = pd.DataFrame({"date": "2021-09-06", "rate": 4.2})

    assert result == df
