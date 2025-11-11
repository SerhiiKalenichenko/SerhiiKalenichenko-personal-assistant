from __future__ import annotations
from datetime import datetime, timedelta
from .models import Contact

def next_birthdays(contacts: list[Contact], within_days: int = 7) -> list[Contact]:
    today = datetime.now().date()
    horizon = today + timedelta(days=within_days)
    result: list[Contact] = []
    for c in contacts:
        if not c.birthday_date:
            continue
        bd = c.birthday_date.date().replace(year=today.year)
        if bd < today:
            bd = bd.replace(year=today.year + 1)
        if today <= bd <= horizon:
            result.append(c)
    return result
