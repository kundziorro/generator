import datetime
import json
import requests
import typing as T


class ExchangeRateRequester:
    def __init__(self):
        self.api_url = "http://api.nbp.pl/api/exchangerates/rates/c/{currency_code}/{start_date}/{end_date}/"

    def get_rate(
        self,
        currency_code="EUR",
        start_date=str(datetime.date.today()),
        end_date=str(datetime.date.today()),
    ) -> list:

        api_url = self.api_url.format(currency_code=currency_code, start_date=start_date, end_date=end_date)

        response = requests.get(api_url).text
        data = json.loads(response)
        return data

    @staticmethod
    def extract_todays_bid(rest_response: dict) -> float:
        todays_rates = rest_response["rates"][0]
        todays_bid = todays_rates["bid"]
        return todays_bid

    @staticmethod
    def extract_historical_bids(rest_response: dict) -> T.Dict[str, float]:
        historical_rates = rest_response["rates"]

        historical_bids = {}
        for rate in historical_rates:
            historical_rate = rate["bid"]
            historical_date = rate["effectiveDate"]
            historical_bids[historical_date] = historical_rate
        return historical_bids

    def get_todays_rate(self) -> float:
        rest_response = self.get_rate()
        todays_bid = self.extract_todays_bid(rest_response)
        return todays_bid

    def get_historical_bids(self, start_date: str, end_date: str = str(datetime.date.today())) -> T.Dict[str, float]:
        rest_response = self.get_rate(start_date=start_date, end_date=end_date)
        historocal_bids = self.extract_historical_bids(rest_response)
        return historocal_bids
