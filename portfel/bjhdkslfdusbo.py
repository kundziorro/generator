import json
import requests
import pandas as pd
import datetime
import ast
import os.path

"""

    currency_api = CurrentNBP()
    tracker = Wallet()
    charts = Visualization()
    hist_api = HistoricalNBP()

    tracker.import_txt()  # this should be in init

    current_rate = currency_api.get_currency("EUR")

    positions = tracker.get_positions()
    to_track = pd.DataFrame(list(positions.items()), columns=["date", "rate"])  # Unused

    overall_profit = {}

    for date in positions:
        pos_profit = current_rate / positions.get(date) - 1
        overall_profit[date] = pos_profit

    tracker_frame = pd.DataFrame(list(overall_profit.items()), columns=["date", "profit"])
    charts.plot_profit_chart(tracker_frame)

    today_date = str(datetime.date.today())
    hist_rates = hist_api.get_hist("EUR", "2021-08-01", today_date)
    hist_frame = pd.DataFrame(list(hist_rates.items()), columns=["date", "rate"])
    charts.plot_hist_chart(hist_frame)

    tracker.add_cash(400)
    result = tracker.get_result()
    result_frame = pd.DataFrame(list(result.items()), columns=["date", "result"])
    charts.plot_wallet_result_PLN(result_frame)

    tracker.export()



"""



class CurrentNBP:
    def __init__(self):
        self.currency = 0
        self.api_url = "http://api.nbp.pl/api/exchangerates/rates/c/{code_in_str}/"


    def get_currency(self, code_in_arg="EUR"):
        # self.code = code
        # api_url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/"
        api_url = self.api_url.format(code_in_str=code_in_arg)

        data_str = requests.get(api_url).text  # TODO change data_str to response
        # data_str = data_json.text
        data_text = json.loads(data_str)
        rate_dict = data_text.get("rates")[0]
        # rate_dict = rate_list[0]
        rate = rate_dict.get("bid")
        # self.currency = rate
        return rate


class HistoricalNBP:
    def __init__(self):
        self.historical = {}

    def get_hist(self, code, start_date, end_date):  # -> dict
        self.code = code
        self.start_date = start_date
        self.end_date = end_date

        hist_url = f"http://api.nbp.pl/api/exchangerates/rates/c/{code}/{start_date}/{end_date}/"

        data_json = requests.get(hist_url)
        data_str = data_json.text
        data_text = json.loads(data_str)
        hist_rates = data_text.get("rates")

        for date in hist_rates:
            self.historical[date.get("effectiveDate")] = date.get("bid")

        return self.historical


class Wallet:
    def __init__(self):
        self.position = {}
        self.result = {}
        self.cash = 0
        
        try:
            with open("d:\python\portfolio\wallet.txt") as file:
                text = file.readlines()
                self.position.update(ast.literal_eval(text[1]))
                self.result.update(ast.literal_eval(text[2]))
                self.cash = int(text[3])
        except FileNotFoundError:
            print("File not found. Creating: wallet.txt")
            with open("d:\python\portfolio\wallet.txt"):pass     



    def add_new_position(self, date, rate):
        # self.date = date
        # self.rate = rate

        self.position[date] = rate

    def get_positions(self): # -> dict:
        return self.position

    def add_cash(self, value_EUR): # TODO: wrong naming convention
        currency_api = CurrentNBP()

        self.cash += value_EUR

        rate = currency_api.get_currency("EUR")
        cash_value = self.cash * rate  # duplicated code with get_cash_value_PLN method
        today_date = str(datetime.date.today())
        self.result[today_date] = cash_value
        self.position[today_date] = rate

    def get_cash_value_PLN(self):  # -> float:
        currency_api = CurrentNBP()
        rate = currency_api.get_currency("EUR")
        cash_value = self.cash * rate
        return cash_value

    def get_result(self):  # -> dict:  # USE property here  https://www.youtube.com/watch?v=jCzT9XFZ5bw
        return self.result

    def export(self): 
        with open("d:/Python/portfolio/wallet.txt", "a") as file:
            file.write(
                f"""
{self.position}
{self.result} 
{self.cash}
             """
            )

class Visualization:
    def __init__(self):
        pass

    def plot_hist_chart(self, data_frame):
        chart_hist = data_frame.plot(x="date", y="rate", kind="line")
        fig_hist = chart_hist.get_figure()
        fig_hist.savefig("hist_chart.png")

    def plot_profit_chart(self, data_frame):
        try:
            chart_profit = data_frame.plot.bar(x="date", y="profit")
            fig_profit = chart_profit.get_figure()
            fig_profit.savefig("profit_chart.png")
        except TypeError:
            pass  # TODO: errors shouldn't pass silently

    def plot_wallet_result_PLN(self, data_frame):
        try:
            chart_result = data_frame.plot(x="date", y="result", kind="line")
            fig_hist = chart_result.get_figure()
            fig_hist.savefig("wallet_chart.png")
        except TypeError:
            pass

if __name__ == "__main__":
    currency_api = CurrentNBP()
    tracker = Wallet()
    charts = Visualization()
    hist_api = HistoricalNBP()

    # tracker.import_txt()  # this should be in init

    current_rate = currency_api.get_currency("EUR")

    positions = tracker.get_positions()
    to_track = pd.DataFrame(list(positions.items()), columns=["date", "rate"])  # Unused

    overall_profit = {}

    for date in positions:
        pos_profit = current_rate / positions.get(date) - 1
        overall_profit[date] = pos_profit

    tracker_frame = pd.DataFrame(list(overall_profit.items()), columns=["date", "profit"])
    charts.plot_profit_chart(tracker_frame)

    today_date = str(datetime.date.today())
    hist_rates = hist_api.get_hist("EUR", "2021-08-01", today_date)
    hist_frame = pd.DataFrame(list(hist_rates.items()), columns=["date", "rate"])
    charts.plot_hist_chart(hist_frame)

    tracker.add_cash(400)
    result = tracker.get_result()
    result_frame = pd.DataFrame(list(result.items()), columns=["date", "result"])
    charts.plot_wallet_result_PLN(result_frame)

    tracker.export()
