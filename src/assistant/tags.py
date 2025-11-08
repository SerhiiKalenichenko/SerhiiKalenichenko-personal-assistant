class TagIndex:
    def __init__(self):
        self._map: dict[str, set[str]] = {}

    def index(self, note_id: str, tags: set[str]) -> None:
        for t in tags:
            self._map.setdefault(t.lower(), set()).add(note_id)

    def remove(self, note_id: str) -> None:
        for ids in self._map.values():
            ids.discard(note_id)

    def update(self, note_id: str, old_tags: set[str], new_tags: set[str]) -> None:
        """Оновлює теги в індексі."""
        for t in old_tags:
            if t.lower() in self._map:
                self._map[t.lower()].discard(note_id)
                if not self._map[t.lower()]:
                    del self._map[t.lower()]
        self.index(note_id, new_tags)

    def search(self, *tags: str) -> set[str]:
        sets = [self._map.get(t.lower(), set()) for t in tags]
        if not sets:
            return set()
        res = sets[0].copy()
        for s in sets[1:]:
            res &= s
        return res

    def sort_by_tags(self, notes: list[dict]) -> list[dict]:
        """Сортує список нотаток за кількістю тегів (спаданням)."""
        return sorted(notes, key=lambda n: len(n.get("tags", [])), reverse=True)

    def clear(self) -> None:
        self._map.clear()
