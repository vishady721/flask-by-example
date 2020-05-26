def date_to_num(datestring):
    month = int(datestring.split('-')[1])
    date = int(datestring.split('-')[2])
    year_num = 43830
    if month == 1:
        month_num = 0
    elif month == 2:
        month_num = 31
    elif month == 3:
        month_num = 31 + 29
    elif month == 4:
        month_num = 31 + 29 + 31
    elif month == 5:
        month_num = 31 + 29 + 31 + 30
    elif month == 6:
        month_num = 31 + 29 + 31 + 30 + 31
    elif month == 7:
        month_num = 31 + 29 + 31 + 30 + 31 + 30
    elif month == 8:
        month_num = 31 + 29 + 31 + 30 + 31 + 30 + 31
    elif month == 9:
        month_num = 31 + 29 + 31 + 39 + 31 + 30 + 31 + 31
    elif month == 10:
        month_num = 31 + 29 + 31 + 39 + 31 + 30 + 31 + 31 + 30
    elif month == 11:
        month_num = 31 + 29 + 31 + 39 + 31 + 30 + 31 + 31 + 30 + 31
    elif month == 12:
        month_num = 31 + 29 + 31 + 39 + 31 + 30 + 31 + 31 + 30 + 31 + 30
    date_num = int(date)
    num = date_num + year_num + month_num
    return num

