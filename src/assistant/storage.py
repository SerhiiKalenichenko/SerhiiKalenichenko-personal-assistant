import os
import pickle
import tempfile
from assistant.addressbook import AddressBook
from assistant.notes import Notebook

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "storage.bin")

class Storage:
    def __init__(self):
        self.ab = AddressBook()
        self.nb = Notebook()
        self.load()

    def load(self):
        if not os.path.exists(DB_FILE):
            return
        with open(DB_FILE, "rb") as f:
            payload = pickle.load(f)
        self.ab.data = payload.get("ab", {})
        self.nb.items = payload.get("nb", [])

    def save(self):
        payload = {"ab": self.ab.data, "nb": self.nb.items}
        fd, tmp = tempfile.mkstemp(dir=DATA_DIR, prefix="storage.", suffix=".tmp")
        try:
            with os.fdopen(fd, "wb") as f:
                pickle.dump(payload, f)
            os.replace(tmp, DB_FILE)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass
