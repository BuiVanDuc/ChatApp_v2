import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_email_validated(email):
    if EMAIL_REGEX.match(email):
        return True
    return False
