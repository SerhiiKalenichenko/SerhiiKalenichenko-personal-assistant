class TagIndex:
    def __init__(self):
        self._map: dict[str, set[str]] = {}

    def index(self, note_id: str, tags: set[str]) -> None:
        for t in tags:
            self._map.setdefault(t.lower(), set()).add(note_id)

    def remove(self, note_id: str) -> None:
        for ids in self._map.values():
            ids.discard(note_id)

    # !!! ЦЕЙ МЕТОД ПОВИНЕН БУТИ ВСЕРЕДИНІ КЛАСУ !!!
    def update(self, note_id: str, old_tags: set[str], new_tags: set[str]) -> None:
        for t in old_tags:
            k = t.lower()
            if k in self._map:
                self._map[k].discard(note_id)
                if not self._map[k]:
                    del self._map[k]
        self.index(note_id, new_tags)

    def search(self, *tags: str) -> set[str]:
        groups = [self._map.get(t.lower(), set()) for t in tags]
        if not groups:
            return set()
        res = groups[0].copy()
        for g in groups[1:]:
            res &= g
        return res

    def sort_by_tags(self, notes: list) -> list:
        """Сортує за зростанням кількості тегів.
        Тай-брейк: за текстом (A..Z). Підтримує dict і об'єкти .text/.tags.
        """
        def grab(n, attr, default):
            return n.get(attr, default) if isinstance(n, dict) else getattr(n, attr, default)

        def key(n):
            tags = grab(n, "tags", [])
            count = len(tags) if isinstance(tags, (set, list, tuple)) else 0
            text = grab(n, "text", "")
            return (count, text.lower())

        return sorted(notes, key=key, reverse=False)

    def clear(self) -> None:
        self._map.clear()
