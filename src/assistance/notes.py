from .models import Note
from typing import Iterable

class NotesRepo:
    def __init__(self, data: Iterable[dict] | None = None):
        self._items: dict[str, Note] = {}
        if data:
            for raw in data:
                n = Note(text=raw.get("text", ""), tags=set(raw.get("tags", [])), id=raw.get("id"))
                self._items[n.id] = n

    def serialize(self) -> list[dict]:
        return [{"id": n.id, "text": n.text, "tags": sorted(n.tags)} for n in self._items.values()]

    def add(self, text: str, tags: set[str] | None = None) -> Note:
        n = Note(text=text, tags=tags or set())
        self._items[n.id] = n
        return n

    def get(self, note_id: str) -> Note:
        return self._items[note_id]

    def update(self, note_id: str, *, text: str | None = None, tags: set[str] | None = None) -> Note:
        n = self._items[note_id]
        if text is not None:
            n.text = text
        if tags is not None:
            n.tags = set(tags)
        return n

    def remove(self, note_id: str) -> None:
        del self._items[note_id]

    def search(self, query: str) -> list[Note]:
        q = query.lower()
        return [n for n in self._items.values() if q in n.text.lower() or any(q in t.lower() for t in n.tags)]
