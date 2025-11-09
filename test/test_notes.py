from assistant.notes import NotesRepo
from assistant.tags import TagIndex

def test_add_and_search_notes():
    repo = NotesRepo()
    n1 = repo.add("Купити батарейки", {"house", "urgent"})
    n2 = repo.add("Подзвонити Івану", {"calls"})
    assert any(n.id == n1.id for n in repo.search("бат"))
    assert any(n.id == n2.id for n in repo.search("дзвон"))

def test_update_and_tags_index():
    repo = NotesRepo()
    n = repo.add("Task", {"a"})
    repo.update(n.id, tags={"a", "b"})
    idx = TagIndex()
    idx.rebuild(list(repo._items.values()))
    by_b = idx.by_tag("b")
    assert any(x.id == n.id for x in by_b)

def test_sort_by_tags():
    repo = NotesRepo()
    repo.add("A", {"a"})
    repo.add("B", {"a", "b"})
    sorted_serialized = repo.sort_by_tags()
    assert [x["text"] for x in sorted_serialized][:2] == ["B", "A"]
