from app import requester


def test_extract_todays_bid():
    exchange_rate_requester = requester.ExchangeRateRequester()
    rest_response = {
        "table": "C",
        "currency": "euro",
        "code": "EUR",
        "rates": [{"no": "173/C/NBP/2021", "effectiveDate": "2021-09-07", "bid": 4.48, "ask": 4.5706}],
    }
    result = exchange_rate_requester.extract_todays_bid(rest_response)

    assert result == 4.48


def test_extract_historical_bids():
    exchange_rate_requester = requester.ExchangeRateRequester()
    rest_response = {
        "table": "C",
        "currency": "euro",
        "code": "EUR",
        "rates": [
            {"no": "173/C/NBP/2021", "effectiveDate": "2021-09-07", "bid": 4.48, "ask": 4.5706},
            {"no": "173/C/NBP/2021", "effectiveDate": "2021-09-06", "bid": 4.51, "ask": 4.56},
        ],
    }
    result = exchange_rate_requester.extract_historical_bids(rest_response)

    assert result == [4.48, 4.51]
