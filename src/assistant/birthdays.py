from __future__ import annotations
from datetime import date, timedelta
from .models import Contact

def upcoming(contacts: list[Contact], within_days: int) -> list[Contact]:
    today = date.today()
    horizon = today + timedelta(days=within_days)
    result = []
    for c in contacts:
        if not c.birthday: continue
        b = c.birthday.replace(year=today.year)
        if b < today:
            b = b.replace(year=today.year + 1)
        if today <= b <= horizon:
            result.append(c)
    return result
