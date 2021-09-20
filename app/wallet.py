from collections import namedtuple

from app.requester import ExchangeRateRequester


Transaction = namedtuple("Transaction", ["date", "value", "rate"])


class Wallet:
    def __init__(self) -> None:
        self.transactions = []
        self.exchange_rate_requester = ExchangeRateRequester()

    def show_transactions(self) -> None:
        for transaction in self.transactions:
            sign = "+" if transaction.value >= 0 else ""
            print(f"In {transaction.date} {sign}{transaction.value} EUR by rate {transaction.rate}")

    def add_buy_transaction(self, date: str, value_euro: float, rate: float) -> None:
        buy = Transaction(date, value_euro, rate)
        self.transactions.append(buy)

    def add_sell_transaction(self, date: str, value_euro: float, rate: float) -> None:
        sell = Transaction(date, value_euro * (-1), rate)
        self.transactions.append(sell)

    def get_value_in_pln(self) -> float:
        todays_rate = self.exchange_rate_requester.get_todays_rate()
        wallet_value = 0
        for transaction in self.transactions:
            wallet_value += transaction.value
        value_in_pln = wallet_value * todays_rate
        return value_in_pln

    def get_paid_value_in_pln(self) -> float:
        transactions_value_pln = 0
        for transaction in self.transactions:
            transactions_value_pln += transaction.value * transaction.rate
        return transactions_value_pln

    def get_profit_in_pln(self) -> float:
        profit = self.get_value_in_pln() - self.get_paid_value_in_pln()
        return profit
