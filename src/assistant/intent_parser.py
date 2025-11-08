from difflib import get_close_matches

ALIASES = {
    "add-contact": ["додай контакт", "створи контакт", "add contact"],
    "find-contact": ["знайди контакт", "пошук контакту", "find contact"],
    "update-contact": ["онови контакт", "редагуй контакт", "update contact"],
    "del-contact": ["видали контакт", "delete contact"],
    "birthdays": ["дні народження", "найближчі дні народження", "birthdays"],
    "add-note": ["додай нотатку", "нова нотатка", "add note"],
    "list-notes": ["список нотаток", "пошук нотаток", "find notes"],
    "update-note": ["онови нотатку", "редагуй нотатку", "update note"],
    "del-note": ["видали нотатку", "delete note"],
    "by-tag": ["за тегом", "нотатки за тегом", "by tag"],
}

def _command_space() -> list[str]:
    base = list(ALIASES.keys())
    for k, vals in ALIASES.items():
        base.extend(vals)
    return base

def guess_intent(raw: str, commands: dict[str, callable]) -> str:
    space = _command_space()
    match = get_close_matches(raw.lower().strip(), space, n=1, cutoff=0.5)
    if not match:
        return ""
    m = match[0]
    if m in commands:
        return m
    for k, vals in ALIASES.items():
        if m in vals and k in commands:
            return k
    return ""
