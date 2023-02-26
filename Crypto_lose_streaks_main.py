import csv
import Crypto_success_rate_classes as cs
import pandas as pd
import time
import os

"""
This program is mostly set to find bigger lose streaks and giving some information about market during trade
"""


def main():
    # Setting names ad positions of columns where we want to save output____________ #

    column_names = [
        "Start price",
        "End price",
        "Lose streak",
        "Time",
        "ma0",
        "ma1",
        "ma2",
    ]
    column_positions = [1, 2, 4, 6, 8, 9, 10]

    # Parameters by which program makes computing
    #############################################################################
    number_of_repetitions = 2
    base_bit = 15
    min_long_time = 70
    starting_short_time = 10

    ma0 = 7
    ma1 = 25
    ma2 = 99
    #############################################################################
    output_excel = cs.ExcelSave(column_names, column_positions)

    for TESTER in range(number_of_repetitions):
        # Init ________________________________________________________________________ #
        sec = 0
        prices_list = []
        min_short_time = TESTER + starting_short_time

        ma_0 = cs.MA(ma0)
        ma_1 = cs.MA(ma1)
        ma_2 = cs.MA(ma2)

        min_short = cs.Min(min_short_time)
        min_long = cs.Min(min_long_time)

        trade = cs.Trade(base_bit)

        output_file_name = f"Output\Lost_streaks{min_short_time},{min_long_time}"

        # Starts reading all the csv files and procesing them _________________________ #
        for num in os.listdir("Trades"):
            with open(f"Trades\{num}") as file:
                file = csv.reader(file)

                for line in file:
                    prices_list.append([float(line[1]), int(line[0]) / 1000])
                    sec += 1

                    ma_0.update(sec, prices_list)
                    ma_1.update(sec, prices_list)
                    ma_2.update(sec, prices_list)
                    if sec > min_long_time:
                        min_short.update(prices_list)
                        min_long.update(prices_list)

                    # updates calculations after min_long_time can be calculated____________________ #
                    if sec > min_long_time:
                        trade.update(
                            prices_list,
                            ma_0.ma,
                            ma_1.ma,
                            ma_2.ma,
                            min_short.min,
                            min_long.min,
                        )

                    if (
                        trade.lose_streak > 4
                        and trade.last_price == trade.end_trade_price
                    ):

                        output_excel.append_to_list(
                            [
                                trade.start_trade_price[0],
                                trade.last_price[0],
                                trade.lose_streak,
                                time.strftime(
                                    "%Y-%m-%d %H:%M:%S",
                                    time.localtime(trade.start_trade_price[1]),
                                ),
                                ma_0.ma,
                                ma_1.ma,
                                ma_2.ma,
                            ]
                        )

        print(f"{int((100/number_of_repetitions)*(TESTER+1))}%")

    # Saves all the information into excel _________________________________________ #
    output_excel.DFrame()
    writer = pd.ExcelWriter(f"{output_file_name}.xlsx", engine="xlsxwriter")
    output_excel.write(writer)
    writer.save()


if __name__ == "__main__":
    main()
