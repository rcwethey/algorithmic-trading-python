from secrets import IEX_CLOUD_API_TOKEN
import os
import sys
import numpy as np
import requests
import math
import xlsxwriter
import pandas as pd


def chunks(lst, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def basic_format_update(key, value):
    new_format = basic_format.copy()
    new_format[f'{key}'] = f'{value}'


# saving our csv file to a varaible to loop over later
stocks = pd.read_csv(os.path.join(
    os.path.dirname(sys.argv[0]), "sp_500_stocks.csv"))

# Adding Our Stocks Data to a Pandas Dataframe
columns = ['Ticker', 'Stock Price',
           'Market Capitalization', 'Number of Shares to Buy']

basic_format = {
    'font_color': '#0a0a23',
    'bg_color': '#ffffff',
    'border': 1
}

sheet_names = ['Recommended Trades']

# Use batch Api calls to increase the performance of the code
# function to split list into sublists

# Get value of portfolio size
while True:
    try:
        portfolio_size = float(input('Enter the value of your portfolio:'))
        break
    except:
        print('That\'s not a number! \nPlease try again! \n')

# takes the 100 length sublists and turns them into lists seperated by comma's
symbol_groups = list(chunks(stocks[columns[0]], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

# initializing Pandas dataframe with column heads
dataframe = pd.DataFrame(columns=columns)

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

# Get how uch you should be investing into each stock
position_size = portfolio_size/len(dataframe.index)

# based on position_size and current share price of each stock, calculate the amount of whole shares you should be purchasing of each stock
for i in range(0, len(dataframe[columns[0]])-1):
    dataframe.loc[i, columns[3]] = math.floor(
        position_size/dataframe[columns[1]][i])

# Initialize our XlxsWriter Object
writer = pd.ExcelWriter('recommended trades.xlsx', engine='xlsxwriter')
dataframe.to_excel(writer, sheet_names[0], index=False)

# Create the formats you need for our Xlsx file
string_format = writer.book.add_format(basic_format)
dollar_format = writer.book.add_format(
    basic_format_update('num_format', '$0.00'))
integer_format = writer.book.add_format(basic_format_update('num_format', '0'))

# create a dictorionary of values to help loop over
columns_formats = {
    'A': [columns[0], string_format],
    'B': [columns[1], dollar_format],
    'C': [columns[2], dollar_format],
    'D': [columns[3], integer_format]
}

# Format
for column in columns_formats.keys():
    writer.sheets[sheet_names[0]].write(
        f'{column}1', columns_formats[column][0], columns_formats[column][1])
    writer.sheets[sheet_names[0]].set_column(
        f'{column}:{column}', 20, columns_formats[column][1])
writer.save()
