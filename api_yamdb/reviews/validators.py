import datetime
import re

from api.utils import ME, PATTERN


def validate_year(year):
    now_year = datetime.date.today().year
    if year > now_year:
        raise ValueError('Нельзя выкладывать ещё не вышедние произведения')
    return year


def validate_username(username):
    if username == ME or not re.match(PATTERN, username):
        raise ValueError('Недопустимое имя')
    return username
