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
        """Безпечне завантаження даних із файлу."""
        if not os.path.exists(DB_FILE):
            return
        try:
            with open(DB_FILE, "rb") as f:
                # Якщо файл порожній — зчитування pickle викличе EOFError
                if os.path.getsize(DB_FILE) == 0:
                    return
                payload = pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            # Якщо файл зіпсований або порожній — створюємо новий
            print("[Warning] storage.bin corrupted or empty. Recreating...")
            self.save()
            return
        self.ab.data = payload.get("ab", {})
        self.nb.items = payload.get("nb", [])

    def save(self):
        """Атомарне збереження даних."""
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
