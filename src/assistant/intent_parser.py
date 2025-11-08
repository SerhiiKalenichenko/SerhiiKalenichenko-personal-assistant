def guess_intent(text: str) -> str:
    s = text.strip().lower()
    if any(k in s for k in ("add contact", "new contact")): return "contacts:add"
    if any(k in s for k in ("find contact", "search contact", "lookup")): return "contacts:search"
    if any(k in s for k in ("add note", "new note")): return "notes:add"
    if any(k in s for k in ("find note", "search note")): return "notes:search"
    if "birthday" in s and "in" in s: return "birthdays:upcoming"
    return "help"

