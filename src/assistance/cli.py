import argparse, sys, os, json
from .storage import JSONStore
from .contacts import AddressBook
from .notes import NotesRepo
from .tags import TagIndex
from .validators import validate_email, validate_phone
from .intent_parser import guess_intent

def _load_state(store: JSONStore) -> tuple[AddressBook, NotesRepo]:
    data = store.load()
    ab = AddressBook(data.get("contacts", []))
    nr = NotesRepo(data.get("notes", []))
    return ab, nr

def _save_state(store: JSONStore, ab: AddressBook, nr: NotesRepo) -> None:
    store.save({"contacts": ab.serialize(), "notes": nr.serialize()})

def _store_from_env() -> JSONStore:
    path = os.environ.get("PA_DB")
    return JSONStore(path=path) if path else JSONStore()

def cli_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pa", description="Personal Assistant CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("add-contact")
    s.add_argument("--name", required=True)
    s.add_argument("--phone", action="append", default=[])
    s.add_argument("--email")
    s.add_argument("--addr")
    s.add_argument("--bday")

    s = sub.add_parser("find-contact")
    s.add_argument("--query", required=True)

    s = sub.add_parser("update-contact")
    s.add_argument("--id", required=True)
    s.add_argument("--name")
    s.add_argument("--phone", action="append")
    s.add_argument("--email")
    s.add_argument("--addr")
    s.add_argument("--bday")

    s = sub.add_parser("del-contact")
    s.add_argument("--id", required=True)

    s = sub.add_parser("birthdays")
    s.add_argument("--in", dest="days", type=int, required=True)

    s = sub.add_parser("add-note")
    s.add_argument("--text", required=True)
    s.add_argument("--tags", default="")

    s = sub.add_parser("list-notes")
    s.add_argument("--query", default="")

    s = sub.add_parser("update-note")
    s.add_argument("--id", required=True)
    s.add_argument("--text")
    s.add_argument("--tags")

    s = sub.add_parser("del-note")
    s.add_argument("--id", required=True)

    s = sub.add_parser("by-tag")
    s.add_argument("--tag", required=True)

    s = sub.add_parser("guess")
    s.add_argument("free_text", nargs=argparse.REMAINDER)

    return p

def _parse_tags(s: str) -> set[str]:
    if not s: return set()
    items = [t.strip() for t in s.replace(";", ",").split(",")]
    return {t for t in items if t}

def _print_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = cli_parser()
    ns = parser.parse_args(argv)

    store = _store_from_env()
    ab, nr = _load_state(store)

    try:
        if ns.cmd == "add-contact":
            email = validate_email(ns.email) if ns.email else None
            phones = [validate_phone(p) for p in ns.phone] if ns.phone else []
            from .models import Contact
            c = Contact(name=ns.name, address=ns.addr, phones=phones, email=email, birthday=None if not ns.bday else ns.bday)
            ab.add(c)
            _save_state(store, ab, nr)
            _print_json({"id": c.id})

        elif ns.cmd == "find-contact":
            res = [{"id": c.id, "name": c.name, "email": c.email, "phones": c.phones, "address": c.address} for c in ab.find(ns.query)]
            _print_json(res)

        elif ns.cmd == "update-contact":
            fields = {}
            for k in ("name", "addr", "bday"):
                v = getattr(ns, k, None)
                if v is not None: fields["address" if k == "addr" else k] = v
            if ns.email is not None:
                fields["email"] = validate_email(ns.email) if ns.email else None
            if ns.phone is not None:
                fields["phones"] = [validate_phone(p) for p in ns.phone] if ns.phone else []
            c = ab.update(ns.id, **fields)
            _save_state(store, ab, nr)
            _print_json({"id": c.id})

        elif ns.cmd == "del-contact":
            ab.remove(ns.id)
            _save_state(store, ab, nr)
            print("OK")

        elif ns.cmd == "birthdays":
            res = [{"id": c.id, "name": c.name} for c in ab.upcoming_birthdays(ns.days)]
            _print_json(res)

        elif ns.cmd == "add-note":
            tags = _parse_tags(ns.tags)
            n = nr.add(ns.text, tags)
            _save_state(store, ab, nr)
            _print_json({"id": n.id})

        elif ns.cmd == "list-notes":
            items = nr.search(ns.query) if ns.query else list(nr._items.values())
            res = [{"id": n.id, "text": n.text, "tags": sorted(n.tags)} for n in items]
            _print_json(res)

        elif ns.cmd == "update-note":
            tags = None if ns.tags is None else _parse_tags(ns.tags)
            n = nr.update(ns.id, text=ns.text, tags=tags)
            _save_state(store, ab, nr)
            _print_json({"id": n.id})

        elif ns.cmd == "del-note":
            nr.remove(ns.id)
            _save_state(store, ab, nr)
            print("OK")

        elif ns.cmd == "by-tag":
            idx = TagIndex()
            notes = list(nr._items.values())
            idx.rebuild(notes)
            res = [{"id": n.id, "text": n.text, "tags": sorted(n.tags)} for n in idx.by_tag(ns.tag)]
            _print_json(res)

        elif ns.cmd == "guess":
            text = " ".join(ns.free_text).strip()
            commands = {k: None for k in ("add-contact","find-contact","update-contact","del-contact","birthdays","add-note","list-notes","update-note","del-note","by-tag")}
            cmd = guess_intent(text, commands)
            print(cmd if cmd else "unknown")

        return 0
    except KeyError:
        print("Not found", file=sys.stderr); return 1
    except ValueError as e:
        print(str(e), file=sys.stderr); return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); return 3

if __name__ == "__main__":
    raise SystemExit(main())
