import csv
import Crypto_success_rate_classes as cs
import pandas as pd
import os

"""
This program calculates how manz trades with setted parameters would be succesfull
and then show percentage of succesfull trades. It also calculates lose streaks during
this time, how big investment it would be to not to lose monez and how big profit we
would have. Program runs number of repetations with slightly increasing duration from
which the program will be taking shorter of 2 lowest prices. This code has been written
for 1s trades, but can be used also for days min, hours etc if we set different input
csv files
"""


def main():
    # Setting names ad positions of columns where we want to save output____________ #

    column_names = [
        "Trades",
        "Won Trades",
        "Percent",
        "ls1",
        "ls2",
        "ls3",
        "ls4",
        "Max ls",
        "Max investment",
        "Profit",
        "Short min",
        "Long min",
    ]
    column_positions = [1, 2, 3, 5, 6, 7, 8, 10, 12, 13, 15, 16]

    # Parameters by which program makes computing
    #############################################################################
    number_of_repetitions = 2
    base_bit = 15
    min_long_time = 60
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

        output_file_name = (
            f"Output\Trades_general {starting_short_time},{min_long_time}"
        )

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

                    # updates calculations after min_long_time can be calculated __________________ #
                    if sec > min_long_time:
                        trade.update(
                            prices_list,
                            ma_0.ma,
                            ma_1.ma,
                            ma_2.ma,
                            min_short.min,
                            min_long.min,
                        )

        output_excel.append_to_list(
            [
                trade.trades,
                trade.success_trades,
                trade.percent,
                trade.lose_streak_list[0],
                trade.lose_streak_list[1],
                trade.lose_streak_list[2],
                trade.lose_streak_list[3],
                trade.max_lose_streak,
                f"{trade.max_investment} $",
                f"{trade.total_profit} $",
                min_short_time,
                min_long_time,
            ]
        )

        print(f"{int((100/number_of_repetitions)*(TESTER+1))}% done")

    # Saves all the information into excel _________________________________________ #
    output_excel.DFrame()
    writer = pd.ExcelWriter(f"{output_file_name}.xlsx", engine="xlsxwriter")
    output_excel.write(writer)

    writer.save()


if __name__ == "__main__":
    main()
