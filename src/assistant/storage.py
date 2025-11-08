import json, os, tempfile, shutil, stat
from typing import Any

class JSONStore:
    def __init__(self, path: str | None = None):
        home = os.path.expanduser("~")
        base = os.path.join(home, ".personal_assistant")
        os.makedirs(base, exist_ok=True)
        self.path = path or os.path.join(base, "db.json")
        if not os.path.exists(self.path):
            self._chmod_base(base)
            self.save({"contacts": [], "notes": []})

    def _chmod_base(self, base: str) -> None:
        try:
            os.chmod(base, stat.S_IRWXU)
        except Exception:
            pass

    def load(self) -> dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: dict[str, Any]) -> None:
        d = os.path.dirname(self.path)
        fd, tmp = tempfile.mkstemp(dir=d)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._rotate_backup()
            os.replace(tmp, self.path)
            try:
                os.chmod(self.path, stat.S_IRUSR | stat.S_IWUSR)
            except Exception:
                pass
        except Exception:
            try: os.remove(tmp)
            except OSError: pass
            raise

    def _rotate_backup(self, keep: int = 3) -> None:
        for i in range(keep, 0, -1):
            src = f"{self.path}.bak{i-1}" if i > 1 else self.path
            dst = f"{self.path}.bak{i}"
            if os.path.exists(src):
                shutil.copy2(src, dst)
