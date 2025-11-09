from __future__ import annotations
from typing import Optional
from .models import Note
from .tags import TagIndex

class NotesRepo:
    def __init__(self) -> None:
        self._items: dict[str, Note] = {}
        self._tags = TagIndex()

    def add(self, text: str, tags: Optional[set[str]] = None) -> Note:
        n = Note(text=text, tags=set(tags or set()))
        self._items[n.id] = n
        self._tags.index(n.id, n.tags)
        return n

    def get(self, note_id: str) -> Optional[Note]:
        return self._items.get(note_id)

    def search(self, query: str) -> list[Note]:
        q = (query or "").lower()
        return [n for n in self._items.values()
                if q in n.text.lower() or any(q in t.lower() for t in n.tags)]

    def update(self, note_id: str, *, text: Optional[str] = None, tags: Optional[set[str]] = None) -> Optional[Note]:
        n = self._items.get(note_id)
        if not n:
            return None
        old_tags = set(n.tags)
        if text is not None:
            n.text = text
        if tags is not None:
            n.tags = set(tags)
            self._tags.update(n.id, old_tags, n.tags)
        return n

    def remove(self, note_id: str) -> bool:
        n = self._items.pop(note_id, None)
        if not n:
            return False
        self._tags.remove(note_id)
        return True

    def sort_by_tags(self) -> list[dict]:
        return self._tags.sort_by_tags([n.serialize() for n in self._items.values()])

    def serialize(self) -> list[dict]:
        return [n.serialize() for n in self._items.values()]
