from secrets import IEX_CLOUD_API_TOKEN
from helper_functions import get_portfolio_size, get_chunks, position_size, read_stocks_file
import numpy as np
from scipy.stats import percentileofscore as score
from statistics import mean
import pandas as pd
import requests
import xlsxwriter

portfolio_size = get_portfolio_size()
stocks = read_stocks_file()
symbol_strings = get_chunks(stocks, 100)

hqm_columns = ['Ticker', 'Stock Price', 'Number of Shares to Buy', 'HQM Score', 'One-Year Price Return', 'One-Year Return Percentile', 'Six-Month Price Return',
               'Six-Month Return Percentile', 'Three-Month Price Return', 'Three-Month Return Percentile', 'One-Month Price Return', 'One-Month Return Percentile', ]

dataframe = pd.DataFrame(columns=hqm_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        dataframe = dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['price'],
                    'N/A',
                    'N/A',
                    data[symbol]['stats']['year1ChangePercent'],
                    'N/A',
                    data[symbol]['stats']['month6ChangePercent'],
                    'N/A',
                    data[symbol]['stats']['month3ChangePercent'],
                    'N/A',
                    data[symbol]['stats']['month1ChangePercent'],
                    'N/A',
                ],
                index=hqm_columns),
            ignore_index=True)

time_periods = ['One-Year', 'Six-Month', 'Three-Month', 'One-Month']

for row in dataframe.index:
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        dataframe.loc[row, percentile_col] = score(
            dataframe[change_col], dataframe.loc[row, change_col])

for row in dataframe.index:
    momentum_percetiles = []
    for time_period in time_periods:
        momentum_percetiles.append(dataframe.loc[
            row, f'{time_period} Return Percentile'])
    dataframe.loc[row, 'HQM Score'] = mean(momentum_percetiles)

dataframe.sort_values('HQM Score', ascending=False, inplace=True)
dataframe = dataframe[:50]
dataframe.reset_index(inplace=True, drop=True)

position_size(portfolio_size, dataframe)
writer = pd.ExcelWriter('momentum_strategy.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer, sheet_name = "Momentum Stategy", index=False)

print(dataframe)
