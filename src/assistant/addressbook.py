from datetime import date
from collections import UserDict
from assistant.models import Contact
from assistant.validators import validate_phone, validate_email, parse_birthday

class AddressBook(UserDict):
    def add(self, contact: Contact):
        self.data[contact.name.lower()] = contact

    def get(self, name: str) -> Contact | None:
        return self.data.get(name.lower())

    def remove(self, name: str) -> bool:
        return self.data.pop(name.lower(), None) is not None

    def find(self, needle: str):
        needle = needle.lower()
        return [c for c in self.data.values() if needle in c.name.lower()]

def add_contact(db, name: str, phone: str = "", email: str | None = None):
    phone = validate_phone(phone) if phone else ""
    email = validate_email(email)
    contact = db.ab.get(name) or Contact(name=name)
    if phone:
        if phone not in contact.phones:
            contact.phones.append(phone)
    contact.email = email or contact.email
    db.ab.add(contact)
    db.save()
    return f"Contact saved: {name}"

def show_contact(db, name: str):
    c = db.ab.get(name)
    if not c:
        return "Not found."
    b = c.birthday.strftime("%d.%m.%Y") if c.birthday else "-"
    return f"{c.name} | phones: {', '.join(c.phones) or '-'} | email: {c.email or '-'} | birthday: {b}"

def show_all(db):
    if not db.ab.data:
        return "No contacts."
    return "\n".join(sorted(show_contact(db, c.name) for c in db.ab.data.values()))

def remove_contact(db, name: str):
    ok = db.ab.remove(name)
    if ok:
        db.save()
    return "Removed." if ok else "Not found."

def add_birthday(db, name: str, birthday: str):
    c = db.ab.get(name)
    if not c:
        return "Not found."
    c.birthday = parse_birthday(birthday)
    db.save()
    return "Birthday set."

def days_to_birthday(db, name: str):
    c = db.ab.get(name)
    if not c or not c.birthday:
        return "No birthday."
    today = date.today()
    bd = c.birthday.replace(year=today.year)
    if bd < today:
        bd = bd.replace(year=today.year + 1)
    return (bd - today).days

def find_contacts(db, needle: str):
    items = db.ab.find(needle)
    if not items:
        return "No matches."
    return "\n".join(show_contact(db, c.name) for c in items)
