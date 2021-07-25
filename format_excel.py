SHEET_NAME = 'Recommended Trades'

basic_format = {
    'font_color': '#0a0a23',
    'bg_color': '#ffffff',
    'border': 1
}


def basic_format_update(key, value):
    new_format = basic_format.copy()
    new_format[f'{key}'] = f'{value}'


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


def format_excelsheet(writer, columns):
    string_format = writer.book.add_format(basic_format)
    dollar_format = writer.book.add_format(
        basic_format_update('num_format', '$0.00'))
    integer_format = writer.book.add_format(
        basic_format_update('num_format', '0'))
    percent_format = writer.book.add_format(
        basic_format_update('num_format', '0.0%'))

    formats = {'string': string_format, 'dollar': dollar_format,
               'int': integer_format, 'percent': percent_format}
    columns_formats = {
        # 'A': [columns[0], string_format],
        # 'B': [columns[1], dollar_format],
        # 'C': [columns[2], dollar_format],
        # 'D': [columns[3], integer_format]
    }

    for index, column in enumerate(columns):
        if "Ticker" in column:
            append_to_columns_formats(
                index, column, columns_formats, formats=formats.get('string'))
        if "Stock" in column:
            print('Yeup')
        if "Market" in column:
            print('Yeup')
        if "Buy" in column:
            print('Yeup')
        if "HQM Score" in column:
            print('Yeup')
        if "Price Return" in column:
            print('Yeup')
        if "Return Percentile" in column:
            print('Yeup')

    print(columns_formats)

    # Format
    for column in columns_formats.keys():
        writer.sheets[SHEET_NAME].write(
            f'{column}1', columns_formats[column][0], columns_formats[column][1])
        writer.sheets[SHEET_NAME].set_column(
            f'{column}:{column}', 20, columns_formats[column][1])


def append_to_columns_formats(index, column, columns_formats, formats):
    return columns_formats[f'{alphabet[index]}'].append(column[index]).extend(formats)
