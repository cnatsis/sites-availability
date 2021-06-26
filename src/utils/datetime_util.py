import datetime


def datetime_convert(o):
    """
    Converts datetime to string
    :param o: datetime object
    :return: datetime to string
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()
