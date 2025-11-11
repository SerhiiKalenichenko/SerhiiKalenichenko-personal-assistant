from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List

@dataclass
class Contact:
    name: str
    phones: list[str] = field(default_factory=list)
    email: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None

@dataclass
class Note:
    text: str
    tags: List[str] = field(default_factory=list)
