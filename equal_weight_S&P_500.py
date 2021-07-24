from secrets import IEX_CLOUD_API_TOKEN
from helper_functions import get_portfolio_size, get_chunks, position_size, read_stocks_file
from format_excel import format_excelsheet, SHEET_NAME
import numpy as np
import requests
import pandas as pd

portfolio_size = get_portfolio_size()
stocks = read_stocks_file()

# Adding Our Stocks Data to a Pandas Dataframe
columns = ['Ticker', 'Stock Price',
           'Market Capitalization', 'Number of Shares to Buy']

dataframe = pd.DataFrame(columns=columns)
symbol_strings = get_chunks(stocks, 100)

# batch api call
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()

    # appending each stock with some parameters to the dataframe
    for symbol in symbol_string.split(','):
        dataframe = dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    data[symbol]['quote']['marketCap'],
                    'N/A'
                ], index=columns),
            ignore_index=True
        )

dataframe = position_size(portfolio_size, dataframe)
writer = pd.ExcelWriter('recommended trades.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer, SHEET_NAME, index=False)
format_excelsheet(writer, columns)
writer.save()
