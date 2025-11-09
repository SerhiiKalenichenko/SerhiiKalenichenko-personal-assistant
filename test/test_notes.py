import pytest
from notes import NotesRepo
from tags import TagIndex


def test_add_note():
    repo = NotesRepo()
    n = repo.add("Hello", set())
    assert n.text == "Hello"
    assert n.tags == set()
    assert n.id in repo._items


def test_add_and_search_notes():
    repo = NotesRepo()
    repo.add("Task A", {"work", "urgent"})
    repo.add("Task B", {"work"})
    repo.add("Task C", {"personal"})
    
    idx = TagIndex()
    idx.rebuild(list(repo._items.values()))
    
    work_notes = idx.by_tag("work")
    assert len(work_notes) == 2


def test_update_and_tags_index():
    repo = NotesRepo()
    n = repo.add("Task", {"a"})
    repo.update(n.id, tags={"a", "b"})
    idx = TagIndex()
    idx.rebuild(list(repo._items.values()))
    
    by_b = idx.by_tag("b")
    assert n.id in by_b


def test_sort_by_tags():
    repo = NotesRepo()
    repo.add("B", {"x", "y", "z"})
    repo.add("A", {"x", "y", "z"})
    
    idx = TagIndex()
    all_notes = list(repo._items.values())
    sorted_notes = idx.sort_by_tags(all_notes)
    
    texts = [n.text for n in sorted_notes]
    assert texts == ["A", "B"]


def test_cli_help_runs():
    """Перевірка, що CLI запускається без помилок"""
    import subprocess
    import sys
    
    result = subprocess.run(
        [sys.executable, "-m", "cli", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0