import datetime


def time_now():
    return f"{datetime.datetime.now():%d_%m_%Y_%H_%M_%S}"
