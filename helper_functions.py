import math
import os
import sys
import pandas as pd
import numpy as np
from statistics import mean
from scipy.stats import percentileofscore as score


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


def fail_safe(denomenator, numerator):
    try:
        final_value = denomenator/numerator
    except TypeError:
        final_value = np.nan
    return final_value


def get_percents(dataframe, list, change_list):
    for row in dataframe.index:
        for list_item in list:
            change_col = f'{list_item} {change_list[0]}'
            percentile_col = f'{list_item} {change_list[1]}'
            dataframe.loc[row, percentile_col] = score(
                dataframe[change_col], dataframe.loc[row, change_col])
    return dataframe


def trim_to_size_and_sort(dataframe, sort_by, trim_to):
    dataframe.sort_values(sort_by, ascending=False, inplace=True)
    dataframe = dataframe[:trim_to]
    dataframe.reset_index(inplace=True, drop=True)
    return dataframe


def get_score(dataframe, list, row_finished_word, score_name):
    for row in dataframe.index:
        momentum_percetiles = []
        for list_item in list:
            momentum_percetiles.append(dataframe.loc[
                row, f'{list_item} {row_finished_word}'])
        dataframe.loc[row, score_name] = mean(momentum_percetiles)
    return dataframe


def filler_data(dataframe, columns):
    for column in columns:
        dataframe[column].fillna(dataframe[column].mean(), inplace=True)
    return dataframe
