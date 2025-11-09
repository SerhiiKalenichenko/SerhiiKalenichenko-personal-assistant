from assistant.notes import NotesRepo
from assistant.tags import TagIndex


def _nid(x):
    return getattr(x, "id", x.get("id") if isinstance(x, dict) else None)


def _text(x):
    return getattr(x, "text", x.get("text") if isinstance(x, dict) else None)


def test_add_and_search_notes():
    repo = NotesRepo()
    n1 = repo.add("Купити батарейки", {"house", "urgent"})
    n2 = repo.add("Подзвонити Івану", {"calls"})
    found = repo.search("купи")
    ids = {_nid(x) for x in found}
    assert n1.id in ids
    assert n2.id not in ids


def test_update_and_tags_index():
    repo = NotesRepo()
    n = repo.add("Task", {"a"})
    repo.update(n.id, tags={"a", "b"})
    idx = TagIndex()

    # rebuild приймає список нотаток (list[Note])
    idx.rebuild(list(repo._items.values()))

    by_b = idx.by_tag("b")
    assert n.id in by_b


def test_sort_by_tags():
    repo = NotesRepo()
    a = repo.add("A", {"a"})
    b = repo.add("B", {"a", "b"})
    sorted_notes = repo.sort_by_tags()
    texts = [_text(x) for x in sorted_notes]
    assert texts[:2] == ["A", "B"]
