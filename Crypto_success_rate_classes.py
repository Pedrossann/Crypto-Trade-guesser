import time
import tkinter as tk
import pandas as pd

"""
Calculates moving avarage.

import: count = sets from how manz variables it should calculate avarage
"""


class MA:
    def __init__(self, count):
        self.count = count
        self.position = 0
        self.total = 0.0
        self.ma = 0

    # Returns moving avarage in int _______________________________________________ #
    def __int__(self):
        return int(self.ma)

    # takes the last "number" of lists in "price_list" and makes moving avarage ____ #
    def avarage(self, sec, price_list):
        if sec > self.count:
            for self.start in range(self.count):
                self.position = -self.start - 1
                self.list = price_list[self.position]
                self.total += self.list[0]
            self.ma = int(int(self.total) / self.count)
            self.total = 0

    def update(self, sec, price_list):
        self.avarage(sec, price_list)


"""
Calculates short minimum in last "count" seconds
"""


class Min:
    def __init__(self, count):
        self.count = count
        self.min = [1000000, 0]

    def minimum(self, price_list):
        self.last_price = price_list[-1]

        if (self.last_price[1] - self.min[1]) >= self.count:
            self.min = [1000000, self.last_price[1] - 100000]
        for num in range(self.count):
            price = price_list[-num - 1]
            if price[0] < self.min[0]:
                self.min = price
        return self.min

    def update(self, price_list):
        self.minimum(price_list)


"""
Holds all the calculation about trading. Separate bools (self.price_min_check, etc) anables for trade to happen.
"""


class Trade:
    def __init__(self, base_bit, trade_delay, delay_diff):
        self.trade_time = 30
        self.trading = False
        self.trading_sec_counter = 0
        self.trades = 0
        self.success_trades = 0
        self.lose_streak = 0

        self.lose_streak_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.win_streak_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.max_lose_streak = 0

        self.delay_diff = delay_diff
        self.trade_delay = trade_delay
        self.base_bit = base_bit
        self.total_profit = 0
        self.max_investment = 0

    # Creates minimal price in last 10 and 50 seconds and anables price_min_check __ #

    def min_check(self, short, long):
        if int(short[0]) == int(long[0]):
            self.price_min_check = False
        else:
            self.price_min_check = True

    # After inputing moving avarages anbles price_ma_check for trading _____________ #
    def ma_check(self, ma_0, ma_1, ma_2):
        if ma_0 == ma_1 and (ma_0 + 7) < ma_2:
            self.price_ma_check = True
        else:
            self.price_ma_check = False

    # If all conditions are met starts trading _____________________________________ #
    def start_trade(self):
        if self.trading == False:
            if self.price_ma_check:
                if self.price_min_check:
                    self.trading = True
                    self.start_trade_price = self.last_price

    # Counts 30 sec of trading and then stops the trading __________________________ #
    def during_trading(self):
        if self.trading == True:
            self.trading_sec_counter += 1
            if self.trading_sec_counter == self.trade_delay:
                if self.delay_diff < self.last_price:
                    self.trading = False
                    self.trading_sec_counter = 0

            if self.trading_sec_counter == 30:
                self.trading = False
                self.trading_sec_counter = 0
                self.end_trade_price = self.last_price
                self.end_trade_check()

    # Counts succesfull trades _____________________________________________________ #
    def end_trade_check(self):
        self.trades += 1
        if self.end_trade_price[0] > self.start_trade_price[0]:
            self.success_trades += 1
            self.lose_streak_list[self.lose_streak] += 1
            if self.max_lose_streak < self.lose_streak:
                self.max_lose_streak = self.lose_streak
            self.total_profit_calculation()
            self.lose_streak = 0
        else:
            self.lose_streak += 1

        self.trade_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(self.start_trade_price[1])
        )
        self.percent = round(self.success_trades / self.trades, 2) * 100

    # Calsulates total profit and max investment ___________________________________ #
    def total_profit_calculation(self):
        cost = self.base_bit
        if self.lose_streak == 0:
            self.total_profit += 15
        else:
            for num in range(self.lose_streak):
                cost = cost + cost * 2
                if cost > self.max_investment:
                    self.max_investment = cost

    # Updates all necessary functions ______________________________________________ #
    def update(self, price_list, ma_0, ma_1, ma_2, short, long):
        self.last_price = price_list[-1]
        self.ma_check(ma_0, ma_1, ma_2)
        self.min_check(short, long)
        self.start_trade()
        self.during_trading()


"""
Saves data to excel
"""


class ExcelSave:
    def __init__(self, column_name_list, start_column_list):
        self.data_list = []
        self.pd_excel = []
        for n in range(len(column_name_list)):
            self.data_list.append([])
            self.pd_excel.append([])
        self.column_name_list = column_name_list
        self.start_col_list = start_column_list

    # Appends variables from list to different columns ______________________________ #
    def append_to_list(self, variable_list):
        for num in range(len(variable_list)):
            self.data_list[num].append(variable_list[num])

    # Writes data from lists to excel _______________________________________________ #
    def DFrame(self):
        for num in range(len(self.data_list)):
            self.pd_excel[num] = pd.DataFrame(
                {f"{self.column_name_list[num]}": self.data_list[num]}
            )

    # Saves data to excel __________________________________________________________ #
    def write(self, writer):
        for num in range(len(self.data_list)):
            self.pd_excel[num].to_excel(
                writer,
                sheet_name="Trades",
                index=False,
                startcol=self.start_col_list[num],
            )
