from .models import Note
from collections import defaultdict

class TagIndex:
    def __init__(self):
        self._idx: dict[str, list[Note]] = defaultdict(list)

    def rebuild(self, notes: list[Note]) -> None:
        self._idx.clear()
        for n in notes:
            for t in n.tags:
                self._idx[t.lower()].append(n)
        for v in self._idx.values():
            v.sort(key=lambda n: (n.text.lower(), n.id))

    def by_tag(self, tag: str) -> list[Note]:
        return list(self._idx.get(tag.lower(), []))

    def sort_by_tags(self, notes: list[Note]) -> list[Note]:
        return sorted(notes, key=lambda n: (sorted([t.lower() for t in n.tags]) or [""], n.text.lower(), n.id))
