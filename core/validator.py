import re

from django.core.exceptions import ValidationError


REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^[a-zA-Z0-9!@#$%^&*+=_]{8,}$' 
REGEX_USERNAME = '^[a-zA-Z0-9]{6,16}$'


def validates_email(email):
    if not re.match(REGEX_EMAIL, email) or email is None:
        raise ValidationError('Invalid Email')

def validates_password(password):
    if not re.match(REGEX_PASSWORD, password) or password is None:
        raise ValidationError('Invalid Password')

def validates_username(username):
    if not re.match(REGEX_USERNAME, username) or username is None:
        raise ValidationError('Invalid Username')

