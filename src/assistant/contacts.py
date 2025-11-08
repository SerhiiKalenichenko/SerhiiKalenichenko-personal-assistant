from __future__ import annotations
from datetime import date
from typing import Any
from .models import Contact

class AddressBook:
    def __init__(self, data: list[dict[str, Any]] | None = None):
        self._records: dict[str, Contact] = {}
        if data:
            for raw in data:
                c = Contact(
                    name=raw.get("name", ""),
                    address=raw.get("address"),
                    phones=raw.get("phones", []),
                    email=raw.get("email"),
                    birthday=raw.get("birthday"),
                    id=raw.get("id"),
                )
                self._records[c.id] = c

    def serialize(self) -> list[dict[str, Any]]:
        return [vars(c) for c in self._records.values()]

    def add(self, contact: Contact) -> None:
        self._records[contact.id] = contact

    def get(self, contact_id: str) -> Contact:
        return self._records[contact_id]

    def remove(self, contact_id: str) -> None:
        del self._records[contact_id]

    def search(self, query: str) -> list[Contact]:
        q = query.lower()
        return [
            c for c in self._records.values()
            if q in c.name.lower()
            or any(q in p.lower() for p in c.phones)
            or (c.email and q in c.email.lower())
        ]
