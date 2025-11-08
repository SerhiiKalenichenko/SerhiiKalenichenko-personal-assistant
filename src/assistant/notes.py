from .tags import TagIndex

class NotesRepo:
    def __init__(self, data=None):
        from .models import Note
        self._items: dict[str, Note] = {}
        self._tags = TagIndex()
        if data:
            for raw in data:
                n = Note(text=raw.get("text", ""),
                         tags=set(raw.get("tags", [])),
                         id=raw.get("id"))
                self._items[n.id] = n
                self._tags.index(n.id, n.tags)

    def add(self, text: str, tags: set[str] | None = None):
        from .models import Note
        n = Note(text=text, tags=tags or set())
        self._items[n.id] = n
        self._tags.index(n.id, n.tags)
        return n

    def update(self, note_id: str, *, text: str | None = None, tags: set[str] | None = None):
        n = self._items[note_id]
        old_tags = n.tags.copy()
        if text is not None:
            n.text = text
        if tags is not None:
            n.tags = set(tags)
            self._tags.update(n.id, old_tags, n.tags)
        return n

    def remove(self, note_id: str) -> None:
        if note_id in self._items:
            self._tags.remove(note_id)
            del self._items[note_id]

    def sort_by_tags(self) -> list[dict]:
        return self._tags.sort_by_tags(self.serialize())
