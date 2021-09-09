import json
import requests


class CurrenciesAPI:

    def __init__(self):
        self.currencies = {}
        
    def get_data(self): 
        api = "http://api.nbp.pl/api/exchangerates/tables/c/"
        data_json = requests.get(api)
        data_str = data_json.text
        data = json.loads(data_str)
        for currency in data:
            self.currencies.update(currency)

    def choose_curr(self, currency_no): # ->dict:  
        choosen_curr = self.currencies.get("rates")
        rates = choosen_curr[currency_no]
        return rates
        
    def show(self):
        print(self.currencies)

    def return_rates(self): # -> list:
        rates = self.currencies.get("rates")
        return rates
        
        
currencyAPI = CurrenciesAPI()
currencyAPI.get_data()

for element in currencyAPI.return_rates():
    print(element)