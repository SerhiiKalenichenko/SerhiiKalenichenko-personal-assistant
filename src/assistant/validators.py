import re
from datetime import datetime

PHONE_RX = re.compile(r"^\+?\d{7,15}$")
EMAIL_RX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_phone(value: str) -> str:
    if not PHONE_RX.match(value):
        raise ValueError("Phone must be 7-15 digits, optional leading +.")
    return value

def validate_email(value: str | None) -> str | None:
    if value is None:
        return None
    if not EMAIL_RX.match(value):
        raise ValueError("Invalid email.")
    return value

def parse_birthday(value: str | None):
    if not value:
        return None
    try:
        # dd.mm.yyyy
        return datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Birthday must be in format dd.mm.yyyy.")
