from datetime import datetime

FORMAT_DATE = {
    'dd-mm-YYYY': '%d-%m-%Y'
}


def convert_string_to_date(date_str, date_format="%d-%m-%Y"):
    try:
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj
    except Exception as ex:
        return None


def convert_datetime_to_string(date_time, format='%H:%M,%d-%m-%Y'):
    if isinstance(date_time, datetime):
        date_time_str = date_time.strftime(format)
        return date_time_str
    print("Input datetime not validate!")
    return None


def get_date_now():
    return datetime.now()
