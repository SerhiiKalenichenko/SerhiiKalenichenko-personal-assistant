from dataclasses import dataclass, field
from datetime import date
from uuid import uuid4

@dataclass
class Contact:
    name: str
    address: str | None = None
    phones: list[str] = field(default_factory=list)
    email: str | None = None
    birthday: date | None = None
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class Note:
    text: str
    tags: set[str] = field(default_factory=set)
    id: str = field(default_factory=lambda: str(uuid4()))
