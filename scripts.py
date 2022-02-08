import re
import string
import random

LETTER_CHOICE = string.ascii_uppercase + string.digits
FORBIDDEN_LETTERS = set(string.punctuation)
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def email_check(email):
    if re.search(regex, email):
        return True
    else:
        return False


def password_check(password):
    setpass = set(list(password))
    if setpass.intersection(FORBIDDEN_LETTERS):
        return False
    else:
        return True


def choicer():
    return ''.join(random.choices(LETTER_CHOICE, k=5))
