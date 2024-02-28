import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            (f'{value} превышает текущее значение. Введите корректный год'),
            params={'value': value},
        )
