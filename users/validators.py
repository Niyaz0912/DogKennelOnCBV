import re
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r'^[A-Za-z0-9]+$')
    if not bool(re.match(pattern, field)):
        print('Must contain A-Z, a-z letters and 0-9 numbers')
        raise ValidationError('Must contain A-Z, a-z letters and 0-9 numbers')
    if not 6 <= len(field) <= 12:
        print('Password length most be between 6 and 12 charters')
        raise ValidationError('Password length most be between 6 and 12 charters')