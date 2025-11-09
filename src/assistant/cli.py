from __future__ import annotations
import argparse, sys, os
from .storage import JSONStore
from .contacts import AddressBook
from .notes import NotesRepo
from .tags import TagIndex
from .validators import validate_email, validate_phone

def _load(store: JSONStore) -> tuple[AddressBook, NotesRepo]:
    data = store.load()
    ab = AddressBook()
    for c in data.get("contacts", []):
        ab.add(
            c.get("name",""),
            address=c.get("address"),
            phones=c.get("phones", []),
            email=c.get("email"),
        )
    nr = NotesRepo()
    for n in data.get("notes", []):
        nr.add(n.get("text",""), set(n.get("tags", [])))
    return ab, nr

def _save(store: JSONStore, ab: AddressBook, nr: NotesRepo) -> None:
    store.save({"contacts": ab.serialize(), "notes": nr.serialize()})

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="assistant", description="Personal CLI Assistant")
    sub = p.add_subparsers(dest="cmd")

    c_add = sub.add_parser("c-add")
    c_add.add_argument("--name", required=True)
    c_add.add_argument("--phone", action="append")
    c_add.add_argument("--email")

    n_add = sub.add_parser("n-add")
    n_add.add_argument("--text", required=True)
    n_add.add_argument("--tag", action="append")

    sub.add_parser("save")
    return p

def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    store = JSONStore()
    ab, nr = _load(store)

    if args.cmd == "c-add":
        phones = [p for p in (args.phone or []) if validate_phone(p)]
        email = args.email if (args.email and validate_email(args.email)) else None
        ab.add(args.name, phones=phones, email=email)
        _save(store, ab, nr)
        return 0

    if args.cmd == "n-add":
        nr.add(args.text, set(args.tag or []))
        _save(store, ab, nr)
        return 0

    if args.cmd == "save":
        _save(store, ab, nr)
        return 0

    parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
