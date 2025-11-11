from __future__ import annotations

ALIASES = {
    "add contact": {"add contact", "new contact", "contact add"},
    "add note": {"add note", "new note", "note add"},
    "find": {"find", "search", "lookup"},
}

def guess_intent(text: str) -> str | None:
    q = (text or "").strip().lower()
    for intent, keys in ALIASES.items():
        if any(k in q for k in keys):
            return intent
    return None
