from __future__ import annotations
from datetime import datetime
from typing import Iterable, Optional
from .models import Contact
from .validators import validate_email, validate_phone

class AddressBook:
    def __init__(self) -> None:
        self._items: dict[str, Contact] = {}

    def add(self, name: str, *, address: Optional[str] = None,
            phones: Optional[Iterable[str]] = None,
            email: Optional[str] = None,
            birthday_date: Optional[datetime] = None) -> Contact:
        phones_list = [p for p in (phones or []) if validate_phone(p)]
        email_ok = email if (email is None or validate_email(email)) else None
        c = Contact(name=name, address=address, phones=phones_list, email=email_ok, birthday_date=birthday_date)
        self._items[c.id] = c
        return c

    def get(self, contact_id: str) -> Optional[Contact]:
        return self._items.get(contact_id)

    def find(self, query: str) -> list[Contact]:
        q = (query or "").lower()
        return [c for c in self._items.values()
                if q in c.name.lower()
                or q in (c.address or "").lower()
                or any(q in p for p in c.phones)
                or (c.email and q in c.email.lower())]

    def update(self, contact_id: str, **fields) -> Optional[Contact]:
        c = self._items.get(contact_id)
        if not c:
            return None
        if "name" in fields and fields["name"]:
            c.name = fields["name"]
        if "address" in fields:
            c.address = fields["address"]
        if "phones" in fields and fields["phones"] is not None:
            c.phones = [p for p in fields["phones"] if validate_phone(p)]
        if "email" in fields:
            c.email = fields["email"] if (fields["email"] and validate_email(fields["email"])) else None
        if "birthday_date" in fields:
            c.birthday_date = fields["birthday_date"]
        return c

    def remove(self, contact_id: str) -> bool:
        return self._items.pop(contact_id, None) is not None

    def serialize(self) -> list[dict]:
        return [c.serialize() for c in self._items.values()]
