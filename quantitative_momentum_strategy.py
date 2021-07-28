from secrets import IEX_CLOUD_API_TOKEN
from helper_functions import get_portfolio_size, get_chunks, position_size, read_stocks_file, get_percents, trim_to_size_and_sort, get_score, filler_data
from format_excel import format_excelsheet
import pandas as pd
import requests

SHEET_NAME = 'Momentum Stategy'
HQM_SCORE = 'HQM_SCORE'

portfolio_size = get_portfolio_size()
stocks = read_stocks_file()
symbol_strings = get_chunks(stocks, 100)

hqm_columns = ['Ticker', 'Stock Price', 'Number of Shares to Buy', HQM_SCORE, 'One-Year Price Return', 'One-Year Return Percentile', 'Six-Month Price Return',
               'Six-Month Return Percentile', 'Three-Month Price Return', 'Three-Month Return Percentile', 'One-Month Price Return', 'One-Month Return Percentile', ]

dataframe = pd.DataFrame(columns=hqm_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        dataframe = dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
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

dataframe = filler_data(dataframe, ['One-Year Price Return', 'Six-Month Price Return',
                        'Three-Month Price Return',  'One-Month Price Return'])

time_periods = ['One-Year', 'Six-Month', 'Three-Month', 'One-Month']

dataframe = get_percents(dataframe, time_periods, [
                         'Price Return', 'Return Percentile'])

dataframe = get_score(dataframe, time_periods, 'Return Percentile', HQM_SCORE)
dataframe = trim_to_size_and_sort(dataframe, HQM_SCORE, 50)
dataframe = position_size(portfolio_size, dataframe)
writer = pd.ExcelWriter('momentum_strategy.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer, SHEET_NAME, index=False)
writer = format_excelsheet(writer, SHEET_NAME, hqm_columns)
writer.save()
