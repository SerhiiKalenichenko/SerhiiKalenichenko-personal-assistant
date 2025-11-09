import re

_EMAIL = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
_PHONE = re.compile(r"^\+?\d{7,15}$")

def validate_email(value: str) -> bool:
    return bool(_EMAIL.match(value or ""))

def validate_phone(value: str) -> bool:
    return bool(_PHONE.match(value or ""))
