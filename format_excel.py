SHEET_NAME = 'Recommended Trades'

basic_format = {
    'font_color': '#0a0a23',
    'bg_color': '#ffffff',
    'border': 1
}


def basic_format_update(key, value):
    new_format = basic_format.copy()
    new_format[f'{key}'] = f'{value}'


def format_excelsheet(writer, columns):
    # Create the formats you need for our Xlsx file
    string_format = writer.book.add_format(basic_format)
    dollar_format = writer.book.add_format(
        basic_format_update('num_format', '$0.00'))
    integer_format = writer.book.add_format(
        basic_format_update('num_format', '0'))

    # create a dictorionary of values to help loop over
    columns_formats = {
        'A': [columns[0], string_format],
        'B': [columns[1], dollar_format],
        'C': [columns[2], dollar_format],
        'D': [columns[3], integer_format]
    }

    # Format
    for column in columns_formats.keys():
        writer.sheets[SHEET_NAME].write(
            f'{column}1', columns_formats[column][0], columns_formats[column][1])
        writer.sheets[SHEET_NAME].set_column(
            f'{column}:{column}', 20, columns_formats[column][1])
