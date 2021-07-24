import math
import os
import sys
import pandas as pd


def read_stocks_file():
    return pd.read_csv(os.path.join(
        os.path.dirname(sys.argv[0]), "sp_500_stocks.csv"))


def chunks(lst, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_portfolio_size():
    # Get value of portfolio size
    while True:
        try:
            portfolio_size = float(input('Enter the value of your portfolio:'))
            break
        except:
            print('That\'s not a number! \nPlease try again! \n')
    return portfolio_size


def get_chunks(stocks, num):
    symbol_groups = list(chunks(stocks['Ticker'], num))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))
    return symbol_strings


def position_size(portfolio_size, dataframe):
    position_size = portfolio_size/len(dataframe.index)
    for i in range(0, len(dataframe['Ticker'])):
        dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(
            position_size/dataframe['Stock Price'][i])
    return dataframe
