def str_standard(text):
    text = str(text)
    return " ".join(text.split())

def str_date_standard(year, month, day):
    year_str = str(year)
    month_str = str(month)
    day_str = str(day)
    if month < 10: month_str = '0'+month_str
    if day < 10: day_str = '0'+day_str
    today_msql = '{}-{}-{}'.format(year_str, month_str, day_str)
    return today_msql