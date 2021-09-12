from pandas.core.frame import DataFrame
from portfel.requester import ExchangeRateRequester
import pandas as pd
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self) -> None:
        self.exchange_rate_requester = ExchangeRateRequester()

    def _get_historical_rates_df(self, transactions) -> DataFrame:
        assert transactions, "There are no transactions"

        first_transaction = transactions[0].date
        historical_rates_date = self.exchange_rate_requester.get_historical_bids(first_transaction)
        df = pd.DataFrame.from_dict(historical_rates_date)

        return df

    def plot_historical_rates(self) -> None:
        plt.plot(self._get_historical_rates_df())
        plt.grid()
        plt.xlabel("date")
        plt.ylabel("rate")
        plt.title("Historical rates")
        plt.tight_layout()
        plt.show()

    def plot_portfolio_value_pln(self, transactions=DataFrame) -> None:
        assert transactions, "There are no transactions"

        df = pd.DataFrame(columns=["date", "portfolio_value_pln"])
        portfolio_value_pln = 0
        for transaction in transactions:
            portfolio_value_pln += transaction.value * transaction.rate
            df = df.append({"date": transaction.date, "portfolio_value_pln": portfolio_value_pln}, ignore_index=True)

        df.set_index(["date"], inplace=True)
        df.plot()
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=55)
        plt.ylabel("value")
        plt.title("Historical portfolio value")
        plt.tight_layout()
        plt.show()

    def plot_profit(self, transactions) -> None:
        assert transactions, "There are no transactions"

        df = self._get_historical_rates_df()
        transaction_rate = transactions.rate
        portfolio_value = transactions.pop(0).value

        for i, row in df.iterrows():

            try:
                if row.date == transactions[0].date:
                    df.at[i, ["transaction_rate"]] = transactions[0].rate
                    transaction_rate = transactions[0].rate
                    portfolio_value += transactions.pop(0).value
                    df.at[i, ["portfolio_value"]] = portfolio_value

                else:
                    df.at[i, ["transaction_rate"]] = transactions[0].rate
                    df.at[i, ["portfolio_value"]] = portfolio_value
            except IndexError:
                df.at[i, ["transaction_rate"]] = transaction_rate
                df.at[i, ["portfolio_value"]] = portfolio_value

        df["value_pln_temp"] = df["portfolio_value"] * df["rate"]
        df["value_pln_after_transaction"] = df["portfolio_value"] * df["transaction_rate"]
        df["profit"] = (df["value_pln_temp"] / df["value_pln_after_transaction"] - 1) * 100

        df.plot(x="date", y="profit")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=45)
        plt.ylabel("profit")
        plt.title("Historical portfolio profit [%]")
        plt.tight_layout()
        plt.show()
