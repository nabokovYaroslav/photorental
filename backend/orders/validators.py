import re
from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_start_date(value):
    tommorow = timezone.now() + timedelta(days=1)
    if value.date() < tommorow.date():
        raise ValidationError(
            "{start_date} <= {now}. Дата начала бронирования должна быть хотя бы на день позже"
            .format(start_date=value.date(), now=tommorow.date())
        )

PHONE_REG = r'^(\+375|80)(29|25|44|33)\d{7}$'

def validate_phone(value):

    if not re.search(PHONE_REG, value):
        raise ValidationError(
            '%(value)s is not a valid value. Phone should be in format (+375|80)(29|25|44|33)XXXXXXX where X is number',
            params={'value': value},
        )