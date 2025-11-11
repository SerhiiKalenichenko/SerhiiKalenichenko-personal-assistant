import sys
from assistant.commands import COMMANDS
from assistant.storage import Storage

def main():
    db = Storage()
    print("Personal Assistant. Type 'help' for commands. 'exit' or 'close' to quit.")
    while True:
        try:
            raw = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        cmd, *args = raw.split()
        if cmd in ("exit", "close"):
            db.save()
            print("Bye.")
            break
        if cmd == "help":
            print("Commands:", ", ".join(sorted(COMMANDS.keys())))
            continue

        handler = COMMANDS.get(cmd)
        if not handler:
            print("Unknown command. Type 'help'.")
            continue

        try:
            result = handler(db, *args)
            if result:
                print(result)
        except Exception as e:
            print(f"Error: {e}")
