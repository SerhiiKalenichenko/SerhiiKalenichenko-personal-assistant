import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
ASSISTANT_DIR = os.path.join(SRC_DIR, "assistant")

for path in (SRC_DIR, ASSISTANT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)
