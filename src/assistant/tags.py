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
        # прибираємо старі
        for t in old_tags:
            key = t.lower()
            if key in self._map:
                self._map[key].discard(note_id)
                if not self._map[key]:
                    del self._map[key]
        # додаємо нові
        self.index(note_id, new_tags)

    def search(self, *tags: str) -> set[str]:
        sets = [self._map.get(t.lower(), set()) for t in tags]
        if not sets:
            return set()
        res = sets[0].copy()
        for s in sets[1:]:
            res &= s
        return res

    def sort_by_tags(self, notes: list) -> list:
        # Підтримує dict і об'єкти з атрибутом .tags
        def tag_count(n) -> int:
            if isinstance(n, dict):
                tags = n.get("tags", [])
            else:
                tags = getattr(n, "tags", [])
            if isinstance(tags, (set, list, tuple)):
                return len(tags)
            return 0
        # ТЕСТ очікує порядок ['A','B'] → зростання
        return sorted(notes, key=tag_count, reverse=False)

    def clear(self) -> None:
        self._map.clear()
