from __future__ import annotations
import json, os, stat
from typing import Any

class JSONStore:
    def __init__(self, path: str | None = None) -> None:
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
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def serialize(items: list) -> list[dict]:
        return [i.serialize() for i in items]
