from secrets import IEX_CLOUD_API_TOKEN
from helper_functions import get_portfolio_size, get_chunks, position_size, read_stocks_file
import numpy as np
from scipy import stats
import pandas as pd
import requests
import xlsxwriter

portfolio_size = get_portfolio_size()
stocks = read_stocks_file()
symbol_strings = get_chunks(stocks, 100)

columns = ['Ticker', 'Stock Price',
           '1 Year Price Return', 'Number of Shares to Buy']

dataframe = pd.DataFrame(columns=columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        dataframe = dataframe.append(
            pd.Series(
                [symbol, data[symbol]['price'], data[symbol]['stats']['year1ChangePercent'], 'N/A'], index=columns), ignore_index=True)

dataframe.sort_values('1 Year Price Return', ascending=False, inplace=True)
dataframe = dataframe[:50]
dataframe.reset_index(inplace=True)

position_size(portfolio_size, dataframe)
print(dataframe)
