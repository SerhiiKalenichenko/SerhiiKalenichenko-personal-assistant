from assistant.addressbook import add_contact, show_contact, show_all, remove_contact, add_birthday, days_to_birthday, find_contacts
from assistant.notes import add_note, list_notes, remove_note, tag_note, search_notes

COMMANDS = {
    "add": add_contact,
    "show": show_contact,
    "all": show_all,
    "remove": remove_contact,
    "birthday": add_birthday,
    "days": days_to_birthday,
    "find": find_contacts,
    "note": add_note,
    "notes": list_notes,
    "delnote": remove_note,
    "tag": tag_note,
    "search": search_notes,
}
