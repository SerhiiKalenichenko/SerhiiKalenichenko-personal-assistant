class TagIndex:
    def __init__(self):
        self._map: dict[str, set[str]] = {}

    def index(self, note_id: str, tags: set[str]) -> None:
        """Додає нові теги до індексу."""
        for t in tags:
            self._map.setdefault(t.lower(), set()).add(note_id)

    def remove(self, note_id: str) -> None:
        """Видаляє замітку з усіх тегів."""
        for ids in self._map.values():
            ids.discard(note_id)

    def update(self, note_id: str, old_tags: set[str], new_tags: set[str]) -> None:
        """Оновлює теги замітки."""
        # видаляємо старі теги
        for t in old_tags:
            if t.lower() in self._map:
                self._map[t.lower()].discard(note_id)
                if not self._map[t.lower()]:
                    del self._map[t.lower()]
        # додаємо нові
        self.index(note_id, new_tags)

    def search(self, *tags: str) -> set[str]:
        """Пошук заміток, які містять усі задані теги."""
        sets = [self._map.get(t.lower(), set()) for t in tags]
        if not sets:
            return set()
        result = sets[0].copy()
        for s in sets[1:]:
            result &= s
        return result

    def sort_by_tags(self, notes: list[dict]) -> list[dict]:
        """Сортує список заміток за кількістю тегів."""
        return sorted(notes, key=lambda n: len(n.get("tags", [])), reverse=True)

    def clear(self) -> None:
        """Очищає індекс."""
        self._map.clear()
