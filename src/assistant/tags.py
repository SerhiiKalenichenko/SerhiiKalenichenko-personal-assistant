class TagIndex:
    def __init__(self):
        self._map: dict[str, set[str]] = {}

    def index(self, note_id: str, tags: set[str]) -> None:
        for t in tags:
            self._map.setdefault(t.lower(), set()).add(note_id)

    def remove(self, note_id: str) -> None:
        for ids in self._map.values():
            ids.discard(note_id)

    def search(self, *tags: str) -> set[str]:
        sets = [self._map.get(t.lower(), set()) for t in tags]
        if not sets: return set()
        out = sets[0].copy()
        for s in sets[1:]:
            out &= s
        return out

    def clear(self) -> None:
        self._map.clear()
