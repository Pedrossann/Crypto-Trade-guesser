import Crypto_success_rate_classes as cs
import random
import pandas as pd

def test_ma_short():
    ma7 = cs.MA(7)

    test_list = [[random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)]]
    num0, num1, num2, num3, num4, num5, num6 = test_list[0], test_list[1], test_list[2], test_list[3], test_list[4], test_list[5], test_list[6]

    ma7.update(10, test_list)
    total = int((num0[0] + num1[0] + num2[0] + num3[0] + num4[0] + num5[0] + num6[0])/7)
    assert ma7.ma == total

def test_ma_long():
    ma14 = cs.MA(14)

    test_list = [[random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)], [random.randint(0,1000000)]]
    num0, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13 = test_list[0], test_list[1], test_list[2], test_list[3], test_list[4], test_list[5], test_list[6], test_list[7], test_list[8], test_list[9], test_list[10], test_list[11], test_list[12], test_list[13]

    ma14.update(28, test_list)
    total = int((num0[0] + num1[0] + num2[0] + num3[0] + num4[0] + num5[0] + num6[0]+ num7[0]+ num8[0]+ num9[0]+ num10[0]+ num11[0]+ num12[0]+ num13[0])/14)
    assert ma14.ma == total

def test_min_short():
    mini = cs.Min(10)

    test_list = [[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0],[random.randint(0,100000),0]]
    price0, price1, price2, price3, price4, price5, price6, price7, price8, price9 = test_list[0], test_list[1], test_list[2], test_list[3], test_list[4], test_list[5], test_list[6], test_list[7], test_list[8], test_list[9]
    price_list = [price0[0], price1[0], price2[0], price3[0], price4[0], price5[0], price6[0], price7[0], price8[0], price9[0]]
    mini.update(test_list)

    assert mini.min[0] == min(price_list)

def test_min_check():
    trade = cs.Trade(15)
    short, long = random.randint(1,3), random.randint(1,3)
    trade.min_check([short,0],[long,0])
    if short == long:
        check = False
    else:
        check = True
    assert trade.price_min_check == check

def test_total_profit_calculation():

    trade = cs.Trade(2)
    trade.lose_streak = 2
    trade.total_profit_calculation()
    assert trade.max_investment == 18

    trade2 = cs.Trade(2)
    trade2.lose_streak = 6
    trade2.total_profit_calculation()
    assert trade2.max_investment == 1458

    trade3 = cs.Trade(2)
    trade3.lose_streak = 3
    trade3.total_profit_calculation()
    assert trade3.max_investment == 54

def test_excel_append():
    data = cs.ExcelSave(["igor","tom", "simon"],[1,2,3])
    writer = pd.ExcelWriter("pokus.xlsx", engine="xlsxwriter")

    data.append_to_list([256, 675, 875])
    data.append_to_list([257, 875, 955])

    data.DFrame()

    data.write(writer)

    writer.save()

    assert data.data_list == [[256,257],[675,875],[875, 955]]
