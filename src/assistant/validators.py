import re

def validate_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?\d{10,15}$", phone))
