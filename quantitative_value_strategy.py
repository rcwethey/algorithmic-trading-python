from secrets import IEX_CLOUD_API_TOKEN
from helper_functions import get_portfolio_size, get_chunks, position_size, read_stocks_file, fail_safe, get_percents, trim_to_size_and_sort, get_score, filler_data
from format_excel import format_excelsheet
import requests
import pandas as pd

SHEET_NAME = 'value_strategy'
PE_RATIO = 'Price to Earnings Ratio'
portfolio_size = get_portfolio_size()
stocks = read_stocks_file()
symbol_strings = get_chunks(stocks, 100)

columns = ['Ticker', 'Stock Price', 'Number of Shares to Buy', PE_RATIO, 'Price to Earnings Percentile', 'Price to Book Ratio',
           'Price to Book Percentile', 'Price to Sales Ratio', 'Price to Sales Percentile', 'EV/EBITDA Ratio', 'EV/EBITDA Percentile', 'EV/GP Ratio', 'EV/GP Percentile', 'RV Score']

dataframe = pd.DataFrame(columns=columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        enterprise_Value = data[symbol]['advanced-stats']['enterpriseValue']
        ebitda = data[symbol]['advanced-stats']['EBITDA']
        gross_profit = data[symbol]['advanced-stats']['grossProfit']

        ev_to_ebitda = fail_safe(enterprise_Value, ebitda)
        ev_to_gp = fail_safe(enterprise_Value, gross_profit)

        dataframe = dataframe.append(
            pd.Series(
                [
                    symbol,
                    data[symbol]['quote']['latestPrice'],
                    'N/A',
                    data[symbol]['quote']['peRatio'],
                    'N/A',
                    data[symbol]['advanced-stats']['priceToBook'],
                    'N/A',
                    data[symbol]['advanced-stats']['priceToSales'],
                    'N/A',
                    ev_to_ebitda,
                    'N/A',
                    ev_to_gp,
                    'N/A',
                    'N/A',
                ],
                index=columns),
            ignore_index=True)

# Fill in missing data
dataframe = filler_data(dataframe, [
                        PE_RATIO, 'Price to Book Ratio', 'Price to Sales Ratio', 'EV/EBITDA Ratio', 'EV/GP Ratio'])

ratios_and_percentiles = ['Price to Earnings', 'Price to Book',
                          'Price to Sales', 'EV/EBITDA', 'EV/GP']

dataframe = get_percents(dataframe, ratios_and_percentiles, [
                         'Ratio', 'Percentile'])
dataframe = get_score(dataframe, ratios_and_percentiles, 'Ratio', 'RV Score')
dataframe = trim_to_size_and_sort(dataframe, PE_RATIO, 50)
dataframe = position_size(portfolio_size, dataframe)
writer = pd.ExcelWriter('quant_value.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer, SHEET_NAME, index=False)
writer = format_excelsheet(writer, SHEET_NAME, columns)
writer.save()
