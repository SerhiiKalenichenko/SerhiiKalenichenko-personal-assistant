class TagIndex:
    def __init__(self):
        self._map: dict[str, set[str]] = {}

    # Додати всі теги нотатки до індексу
    def index(self, note_id: str, tags: set[str]) -> None:
        for t in tags:
            self._map.setdefault(t.lower(), set()).add(note_id)

    # Прибрати нотатку з усіх тегів
    def remove(self, note_id: str) -> None:
        for ids in self._map.values():
            ids.discard(note_id)

    # Оновити теги нотатки (старі -> нові)
    def update(self, note_id: str, old_tags: set[str], new_tags: set[str]) -> None:
        for t in old_tags:
            key = t.lower()
            if key in self._map:
                self._map[key].discard(note_id)
                if not self._map[key]:
                    del self._map[key]
        self.index(note_id, new_tags)

    # Пошук перетину по тегах
    def search(self, *tags: str) -> set[str]:
        sets = [self._map.get(t.lower(), set()) for t in tags]
        if not sets:
            return set()
        res = sets[0].copy()
        for s in sets[1:]:
            res &= s
        return res

    # Сортування списку нотаток за кількістю тегів (підтримує dict і Note)
    def sort_by_tags(self, notes: list) -> list:
        def tag_count(n) -> int:
            # dict-нотатка
            if isinstance(n, dict):
                tags = n.get("tags", [])
                return len(tags if isinstance(tags, (list, set, tuple)) else [])
            # об'єкт Note
            tags = getattr(n, "tags", set())
            return len(tags if isinstance(tags, (set, list, tuple)) else [])
        return sorted(notes, key=tag_count, reverse=True)

    def clear(self) -> None:
        self._map.clear()
