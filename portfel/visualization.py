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
        df = pd.DataFrame.from_dict(historical_rates_date)

        plt.plot(df)
        plt.grid()
        plt.xlabel("date")
        plt.ylabel("rate")
        plt.title("Historical rates")
        plt.show()

    def plot_portfolio_value_pln(self, transactions) -> None:
        assert transactions, "There are no transactions"

        df = pd.DataFrame(columns=["date", "portfolio_value_pln"])
        portfolio_value = 0
        for transaction in transactions:
            portfolio_value += transaction.value * transaction.rate
            df = df.append({"date": transaction.date, "portfolio_value_pln": portfolio_value}, ignore_index=True)

        df.set_index(["date"], inplace=True)
        df.plot()
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=55)
        plt.ylabel("value")
        plt.title("Historical portfolio value")
        plt.show()

    def plot_profit(self, transactions) -> None:
        assert transactions, "There are no transactions"
