import re

from django.core.exceptions import ValidationError

from users.models           import User

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^.*(?=^.{8,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$'
REGEX_USERNAME = '^[a-zA-Z0-9]{6,16}$'
REGEX_CONTACT  = '^\d{2,3}-\d{3,4}-\d{4}$'

def validates_email(email):
    if not re.match(REGEX_EMAIL, email) or email is None:
        raise ValidationError('Invalid Email')

def validates_password(password):
    if not re.match(REGEX_PASSWORD, password) or password is None:
        raise ValidationError('Invalid Password')

def validates_username(username):
    if not re.match(REGEX_USERNAME, username) or username is None:
        raise ValidationError('Invalid Username')

def validates_contact(contact):
    if not re.match(REGEX_CONTACT, contact) or contact is None:
        raise ValidationError('Invalid Contact')