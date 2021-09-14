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
        df = pd.DataFrame(list(historical_rates_date.items()), columns=["date", "rate"])

        return df

    def plot_historical_rates(self, data_frame) -> None:
        data_frame.plot(x="date", y="rate")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=45)
        plt.ylabel("rate")
        plt.title("Historical rates")
        plt.tight_layout()
        plt.show()

    def plot_portfolio_value_pln(self, transactions=DataFrame) -> None:
        if transactions.empty:
            print("There are no transactions")
            return

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

    def plot_profit(self, transactions, data_frame) -> None:
        assert transactions, "There are no transactions"

        transaction_rate = transactions[0].rate
        portfolio_value = transactions.pop(0).value

        for i, row in data_frame.iterrows():

            try:
                if row.date == transactions[0].date:
                    data_frame.at[i, ["transaction_rate"]] = transactions[0].rate
                    transaction_rate = transactions[0].rate
                    portfolio_value += transactions.pop(0).value
                    data_frame.at[i, ["portfolio_value"]] = portfolio_value
                else:
                    data_frame.at[i, ["transaction_rate"]] = transactions[0].rate
                    data_frame.at[i, ["portfolio_value"]] = portfolio_value
            except IndexError:
                data_frame.at[i, ["transaction_rate"]] = transaction_rate
                data_frame.at[i, ["portfolio_value"]] = portfolio_value

        data_frame["value_pln_temp"] = data_frame["portfolio_value"] * data_frame["rate"]
        data_frame["value_pln_after_transaction"] = data_frame["portfolio_value"] * data_frame["transaction_rate"]
        data_frame["profit"] = (data_frame["value_pln_temp"] / data_frame["value_pln_after_transaction"] - 1) * 100

        data_frame.plot(x="date", y="profit")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=45)
        plt.ylabel("profit")
        plt.title("Historical portfolio profit [%]")
        plt.tight_layout()
        plt.show()
