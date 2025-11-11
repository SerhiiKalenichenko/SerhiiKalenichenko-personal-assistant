from assistant.models import Note

class Notebook:
    def __init__(self):
        self.items: list[Note] = []

    def add(self, text: str):
        n = Note(text=text)
        self.items.append(n)
        return n

    def remove(self, idx: int) -> bool:
        if 0 <= idx < len(self.items):
            del self.items[idx]
            return True
        return False

    def search(self, needle: str):
        needle = needle.lower()
        return [n for n in self.items if needle in n.text.lower() or any(needle in t.lower() for t in n.tags)]

def add_note(db, *words):
    text = " ".join(words)
    db.nb.add(text)
    db.save()
    return "Note added."

def list_notes(db):
    if not db.nb.items:
        return "No notes."
    lines = []
    for i, n in enumerate(db.nb.items, 1):
        tag_str = f" [{', '.join(n.tags)}]" if n.tags else ""
        lines.append(f"{i}. {n.text}{tag_str}")
    return "\n".join(lines)

def remove_note(db, index: str):
    ok = db.nb.remove(int(index) - 1)
    if ok:
        db.save()
    return "Removed." if ok else "Not found."

def tag_note(db, index: str, *tags):
    i = int(index) - 1
    if 0 <= i < len(db.nb.items):
        note = db.nb.items[i]
        for t in tags:
            if t not in note.tags:
                note.tags.append(t)
        db.save()
        return "Tagged."
    return "Not found."

def search_notes(db, *words):
    needle = " ".join(words)
    items = db.nb.search(needle)
    if not items:
        return "No matches."
    return "\n".join(n.text for n in items)
