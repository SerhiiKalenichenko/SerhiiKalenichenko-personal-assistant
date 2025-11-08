from assistant.notes import NotesRepo
from assistant.tags import TagIndex

def test_add_and_search_notes():
    repo = NotesRepo()
    n1 = repo.add("Купити батарейки", {"house", "urgent"})
    n2 = repo.add("Подзвонити Івану", {"calls"})
    assert any(n.id == n1.id for n in repo.search("батар"))
    assert any(n.id == n2.id for n in repo.search("Іван"))

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
    n1 = repo.add("B", {"b"})
    n2 = repo.add("A", {"a"})
    idx = TagIndex()
    sorted_notes = idx.sort_by_tags([n1, n2])
    assert [n.text for n in sorted_notes] == ["A", "B"]
