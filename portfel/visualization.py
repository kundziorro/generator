from portfel.requester import ExchangeRateRequester
import pandas as pd
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self) -> None:
        self.exchange_rate_requester = ExchangeRateRequester()

    def plot_historical_rates(self, transactions) -> None:
        assert transactions, "There are no transactions"

        first_transaction = transactions[0].date
        historical_rates_date = self.exchange_rate_requester.get_historical_bids(first_transaction)
        df = pd.DateFrame(list(historical_rates_date.items()), columns=["date", "rate"])

        df.plot.line()
        plt.grid()
        plt.xlabel("date", rotation=90)
        plt.ylabel("rate")
        plt.title("Historical rates")
        df.show()

    def plot_portfolio_value_pln(self, transactions) -> None:
        assert transactions, "There are no transactions"

        df = pd.DataFrame(columns=["date", "portfolio_value_pln"])
        portfolio_value = 0
        for transaction in transactions:
            portfolio_value += transaction.value
            df["date"] = transaction.date
            df["portfolio_value_pln"] = portfolio_value * transaction.rate

        df.plot.line()
        plt.xlabel("date", rotation=90)
        plt.ylabel("value")
        plt.title("Historical portfolio value")
        df.show()

    def plot_profit(self, profit) -> None:
        profit.plot.bar()
        plt.ylabel("value")
        plt.title("Portfolio profit")
        profit.show()
