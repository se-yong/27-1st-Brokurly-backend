import re

from django.core.exceptions import ValidationError

from users.models           import User

REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
# 대,소문자, 숫자, -, _, ., 허용, (@, .) 필수 입력
REGEX_PASSWORD = '/^.*(?=^.{8,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$/'
# 대,소문자, 숫자 그리고 괄호를 제외한 1개 이상의 특수문자 필요, 8자리 이상, 15자리 이하 비밀번호
REGEX_USERNAME = '/^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{4,10}$/'
# 대,소문자, 숫자, 특문포함
REGEX_CONTACT = '/^\d{2,3}-\d{3,4}-\d{4}$/'
# 앞자리 2~3자리 가능(폰번호 대신 집전화 쓸 수도 있어서)

def validates_email(email):
    if not re.match(REGEX_EMAIL, email) or email is None:
        raise ValidationError(
            'Invalid Email'
        )

    if User.objects.filter(email=email).exists():
        raise ValidationError(
            'Duplicated Email Exists'
        )

def validates_password(password):
    if not re.match(REGEX_PASSWORD, password) or password is None:
        raise ValidationError(
            'Invalid Password'
        )

def validates_username(username):
    if not re.match(REGEX_USERNAME, username) or username is None:
        raise ValidationError(
            'Invalid Username'
        )

    if User.objects.filter(username=username).exists():
        raise ValidationError(
            'Duplicated Username Exists'
        )

def validates_contact(contact):
    if not re.match(REGEX_CONTACT, contact) or contact is None:
        raise ValidationError(
            'Invalid Contact'
        )