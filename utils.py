import radar
import datetime
import random


def get_random_date(min, max):
    return radar.random_date(start=min, stop=max)


def get_random_time(min=None):
    return radar.random_time(start=min)


def get_random_date_from_year(year):
    return datetime.date(year=year, month=random.randint(1, 12), day=random.randint(1, 28))
