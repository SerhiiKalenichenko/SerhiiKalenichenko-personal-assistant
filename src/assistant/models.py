from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Contact:
    name: str
    address: Optional[str] = None
    phones: list[str] = field(default_factory=list)
    email: Optional[str] = None
    birthday_date: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phones": list(self.phones),
            "email": self.email,
            "birthday_date": self.birthday_date.isoformat() if self.birthday_date else None,
        }

@dataclass
class Note:
    text: str
    tags: set[str] = field(default_factory=set)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def serialize(self) -> dict:
        return {"id": self.id, "text": self.text, "tags": sorted(self.tags)}
