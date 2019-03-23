import datetime

FORMAT_DATE = {
    'dd-mm-YYYY': '%d-%m-%Y',
    'H:m, dd-mm-yyyy': '%d-%m-%Y'
}

TYPE_DATE_TIME = (datetime, datetime.date, datetime.time)


def convert_string_to_date(date_str, format="%d-%m-%Y"):
    try:
        date_obj = datetime.strptime(date_str, format)
        return date_obj
    except Exception as ex:
        return None


def convert_datetime_to_string(date_time, format='%H:%M,%d-%m-%Y'):
    if type(date_time) in TYPE_DATE_TIME:
        date_time_str = date_time.strftime(format)
        return date_time_str
    print("Input datetime not validate!")
    return None


def get_date_now():
    return datetime.now()
