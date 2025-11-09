from __future__ import annotations
from typing import Iterable, Dict, Set
from .models import Note

class TagIndex:
    def __init__(self) -> None:
        self._map: Dict[str, Set[str]] = {}
        self._id_to_note: Dict[str, Note] = {}

    def index(self, note_id: str, tags: set[str]) -> None:
        for t in tags:
            self._map.setdefault(t, set()).add(note_id)

    def update(self, note_id: str, old: set[str], new: set[str]) -> None:
        removed = old - new
        added = new - old
        for t in removed:
            s = self._map.get(t)
            if s:
                s.discard(note_id)
                if not s:
                    self._map.pop(t, None)
        for t in added:
            self._map.setdefault(t, set()).add(note_id)

    def remove(self, note_id: str) -> None:
        for s in self._map.values():
            s.discard(note_id)

    def by_tag(self, tag: str) -> set[Note]:
        ids = self._map.get(tag, set())
        return {self._id_to_note[i] for i in ids if i in self._id_to_note}

    def rebuild(self, notes: Iterable[Note]) -> None:
        self._map.clear()
        self._id_to_note = {n.id: n for n in notes}
        for n in notes:
            self.index(n.id, set(n.tags))

    def sort_by_tags(self, notes: list[dict]) -> list[dict]:
        return sorted(notes, key=lambda n: len(n.get("tags", [])), reverse=True)

    def clear(self) -> None:
        self._map.clear()
        self._id_to_note.clear()
