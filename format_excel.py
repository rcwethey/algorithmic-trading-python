alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

basic_format = {
    'font_color': '#0a0a23',
    'bg_color': '#ffffff',
    'border': 1
}


def basic_format_update(key, value):
    new_format = basic_format.copy()
    new_format[f'{key}'] = f'{value}'
    return new_format


def type_formats():
    string_format = basic_format
    dollar_format = basic_format_update('num_format', '$0.00')
    integer_format = basic_format_update('num_format', '0')
    float_format = basic_format_update('num_format', '0.0')
    percent_format = basic_format_update('num_format', '0.0%')
    return {'string': string_format, 'dollar': dollar_format, 'int': integer_format, 'float': float_format, 'percent': percent_format}


def append_to_columns_formats(writer, index, column, columns_formats, formats):
    new_columns_formats = wrap_column_formats_in_writer(
        writer, formats)
    columns_formats[f'{alphabet[index]}'] = [f'{column}', new_columns_formats]
    return columns_formats


def wrap_column_formats_in_writer(writer, columns_formats):
    new_writer = writer.book.add_format(columns_formats)
    return new_writer


def format_columns(writer, sheet_name, columns_formats):
    for column in columns_formats.keys():
        writer.sheets[sheet_name].write(
            f'{column}1', columns_formats[column][0], columns_formats[column][1])
        writer.sheets[sheet_name].set_column(
            f'{column}:{column}', 20, columns_formats[column][1])
    return writer


def format_excelsheet(writer, sheet_name, columns):
    formats = type_formats()
    columns_formats = {}

    for index, column in enumerate(columns):
        if "Ticker" in column:
            append_to_columns_formats(
                writer, index, column, columns_formats, formats=formats.get('string'))
        if any(x in column for x in ("Stock", "Market")):
            append_to_columns_formats(
                writer, index, column, columns_formats, formats=formats.get('dollar'))
        if "Number" in column:
            append_to_columns_formats(
                writer, index, column, columns_formats, formats=formats.get('int'))
        if "Ratio" in column:
            append_to_columns_formats(
                writer, index, column, columns_formats, formats=formats.get('float'))
        if any(x in column for x in ("Score", "Percentile", "Price Return")):
            append_to_columns_formats(
                writer, index, column, columns_formats, formats=formats.get('percent'))

    writer = format_columns(writer, sheet_name, columns_formats)
    return writer
