from collections import namedtuple

from portfel.requester import ExchangeRateRequester

Transaction = namedtuple("Transaction", ["date", "value"])


class Wallet:
    def __init__(self):
        self.transactions = []
        self.exchange_rate_requester = ExchangeRateRequester()

    def show_transactions(self):
        pass

    def add_buy_transaction(self, value_euro, date):
        buy = Transaction(date, value_euro)
        self.transactions.append(buy)

    def add_sell_transaction(self, value_euro, date):
        sell = Transaction(date, value_euro*(-1))
        sell = sell
        self.transactions.append(sell)

    def get_value_in_pln(self):
        todays_rate = self.exchange_rate_requester.get_todays_rate()
        wallet_value = 0
        for transaction in self.transactions:
            wallet_value += transaction.value
        value_in_pln = wallet_value * todays_rate
        return value_in_pln

    def get_paid_value_in_pln(self):
        pass

    def get_profit_in_pln(self):
        pass
