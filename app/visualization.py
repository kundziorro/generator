from requester import ExchangeRateRequester
import pandas as pd
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self) -> None:
        self.exchange_rate_requester = ExchangeRateRequester()

    def _historical_rates_df(self, transactions) -> pd.DataFrame:
        assert transactions, "There are no transactions"

        first_transaction = transactions[0].date
        historical_rates_date = self.exchange_rate_requester.get_historical_bids(first_transaction)
        historical_rates_df = pd.DataFrame(list(historical_rates_date.items()), columns=["date", "rate"])

        return historical_rates_df

    def _operations_df(self, transactions: list) -> pd.DataFrame:
        assert transactions, "There are no transactions"

        operations_df = self._historical_rates_df(transactions)

        transaction_rate = transactions[0].rate
        portfolio_value = transactions.pop(0).value

        for i, row in operations_df.iterrows():

            try:
                if row.date == transactions[0].date:
                    operations_df.at[i, ["transaction_rate"]] = transactions[0].rate
                    transaction_rate = transactions[0].rate
                    portfolio_value += transactions.pop(0).value
                    operations_df.at[i, ["portfolio_value"]] = portfolio_value
                else:
                    operations_df.at[i, ["transaction_rate"]] = transactions[0].rate
                    operations_df.at[i, ["portfolio_value"]] = portfolio_value
            except IndexError:
                operations_df.at[i, ["transaction_rate"]] = transaction_rate
                operations_df.at[i, ["portfolio_value"]] = portfolio_value

        operations_df["value_pln_temp"] = operations_df["portfolio_value"] * operations_df["rate"]
        operations_df["value_pln_after_transaction"] = (
            operations_df["portfolio_value"] * operations_df["transaction_rate"]
        )
        operations_df["profit"] = (
            operations_df["value_pln_temp"] / operations_df["value_pln_after_transaction"] - 1
        ) * 100
        return operations_df

    def _operations_df_smaller_list(self, transactions: list) -> pd.DataFrame:
        assert transactions, "There are no transactions"

        operations_df = self._historical_rates_df(transactions)
        operations_df["transaction[+/-]"] = 0
        operations_df["transaction_rate"] = 0

        for transaction in transactions:
            operations_df.loc[operations_df["date"] == transaction.date, "transaction[+/-]"] = transaction.value
            operations_df.loc[operations_df["date"] == transaction.date, "transaction_rate"] = transaction.rate

        operations_df["portfolio_value"] = operations_df["transaction[+/-]"].cumsum()
        operations_df["transaction_rate"] = operations_df["transaction_rate"].mask(
            operations_df["transaction_rate"] == 0,
            operations_df["transaction_rate"].shift(1, fill_value=transactions[0].rate),
        )

        operations_df["value_pln_after_transaction"] = (
            operations_df["portfolio_value"] * operations_df["transaction_rate"]
        )
        operations_df["profit"] = (
            operations_df["value_pln_temp"] / operations_df["value_pln_after_transaction"] - 1
        ) * 100
        return operations_df

    def _operations_df_without_for(self, transactions: list) -> pd.DataFrame:
        assert transactions, "There are no transactions"

        operations_df = self._historical_rates_df(transactions)
        transactions_df = pd.DataFrame(transactions, columns=["date", "transaction[+/-]", "transaction_rate"])
        operations_df = pd.merge(operations_df, transactions_df, on="date", how="outer").fillna(0)

        operations_df["portfolio_value"] = operations_df["transaction[+/-]"].cumsum()
        operations_df["transaction_rate"] = operations_df["transaction_rate"].mask(
            operations_df["transaction_rate"] == 0,
            operations_df["transaction_rate"].shift(1, fill_value=transactions[0].rate),
        )

        operations_df["value_pln_after_transaction"] = (
            operations_df["portfolio_value"] * operations_df["transaction_rate"]
        )
        operations_df["profit"] = (
            operations_df["value_pln_temp"] / operations_df["value_pln_after_transaction"] - 1
        ) * 100
        return operations_df

    def plot_historical_rates(self, historical_rates: pd.DataFrame) -> None:
        historical_rates.plot(x="date", y="rate")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=45)
        plt.ylabel("rate")
        plt.title("Historical rates [PLN]")
        plt.tight_layout()
        plt.show()

    def plot_portfolio_value_pln(self, operations: pd.DataFrame) -> None:
        operations.plot(x="date", y="value_pln_temp")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=55)
        plt.ylabel("value")
        plt.title("Historical portfolio value [PLN]")
        plt.tight_layout()
        plt.show()

    def plot_profit(self, operations: pd.DataFrame) -> None:
        operations.plot(x="date", y="profit")
        plt.grid()
        plt.xlabel("date")
        plt.xticks(rotation=45)
        plt.ylabel("profit")
        plt.title("Historical portfolio profit [%]")
        plt.tight_layout()
        plt.show()
