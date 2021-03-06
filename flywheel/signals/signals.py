import json
import matplotlib.pyplot as plt
import os
import sys
import imp
from flywheel.settings import STOCK_LIST
from flywheel.utils import matplot
from flywheel.market.market import Market

from datetime import date
from datetime import datetime

DUMMY_DATA_PATH = "flywheel/market/stock_data.json"
MOD_CANDIDATES = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]

market = Market()

registered_signals = ['MACD']

def compute(ticker):
    pass

# Backtesting done offlines
def recommend(ticker):
    # Access signals and then make buy decisions.
    recommenation = ''#'BUY+'/'BUY'/'HOLD'/'SELL'/'SELL+'
    return recommenation

def get_price():
    with open(DUMMY_DATA_PATH, 'r') as json_file:
        stock_data = json.load(json_file)
        return stock_data

def process_market_data(market_data):
    print(STOCK_LIST)
    flag = True
    for ticker in STOCK_LIST:
        formatted_data = market.get_history(ticker)
        #print(formatted_data)
        ema = get_ema(formatted_data, "Close")
        ema_dif = get_ema_dif(ema, 7, 14)
        macd = get_macd(ema_dif, 9)
        data = []
        original_data = []
        for data_daily in formatted_data.values():
            original_data.append(data_daily["Close"])
        data.append(original_data)
        data.append(ema.values())
        data.append(ema_dif.values())
        data.append(macd.values())
        #print(data)
        if flag:
            matplot.lineplot(ema.keys(), data, title=ticker)
            #flag = False

# return dict{zip(date, ema)}        
def get_ema(stock_data, mod):
    ema = {}
    N = 0
    ema_t0 = 0
    for date in stock_data:
        stock_data_daily = stock_data[date]
        N += 1
        alpha = 2.0 / (N + 1)
        ema_t1 = ema_t0 + alpha * (stock_data_daily[mod] - ema_t0)
        ema[date] = ema_t1
        ema_t0 = ema_t1
    return ema

# return dict{zip(date, ema_dif)}
def get_ema_dif(ema_dict, day_range_alpha, day_range_beta):
    ema_tuples = list(ema_dict.items())
    ema_dif = {}
    ema_slow = 0
    ema_fast = 0
    slow_head = 0
    fast_head = 0
    N_slow = 0
    N_fast = 0
    for i in range(len(ema_tuples)):
        N_fast += 1
        N_slow += 1
        date, ema = ema_tuples[i]
        ema_dif[date] = 0
        if (N_fast >= day_range_alpha):
            N_fast = day_range_alpha
            ema_fast = culmulative_range_average(ema_fast, N_fast, ema, ema_tuples[fast_head][1])
            fast_head += 1
        else:
            ema_fast = culmulative_range_average(ema_fast, N_fast, ema, 0)
        if (N_slow >= day_range_beta):
            N_slow = day_range_beta
            ema_slow = culmulative_range_average(ema_slow, N_slow, ema, ema_tuples[slow_head][1])
            slow_head += 1
            ema_dif[date] = ema_slow - ema_fast
        else:
            ema_slow = culmulative_range_average(ema_slow, N_slow, ema, 0)
    return ema_dif

def get_macd(ema_dif, day_range):
    macd = {}
    ema_tuples = list(ema_dif.items())
    N = 0
    head = 0
    ema_culmulative = 0
    for i in range(len(ema_tuples)):
        N += 1
        date, ema = ema_tuples[i]
        macd[date] = 0
        if (N >= day_range):
            N = day_range
            ema_culmulative = culmulative_range_average(ema_culmulative, N, ema, ema_tuples[head][1])
            head += 1
            macd[date] = ema_culmulative
        else:
            ema_culmulative = culmulative_range_average(ema_culmulative, N, ema, 0)
    return macd    

def culmulative_range_average(pre_average, N, new_value, old_value):
    return pre_average + (new_value - old_value) / N

def testplot():
    plt.subplots(1, 1)
    x= range(100)
    y= [i**2 for i in x]

    plt.plot(x, y, linewidth = '1', label = "test", color='#539caf', linestyle=':', marker='|')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    #print(sys.path)
    #print(os.getcwd())
    #print(get_price("msft"))
    market_data = get_price()
    process_market_data(market_data)
    #testplot()