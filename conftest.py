import sys, os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(BASE_DIR, "src")
ASSISTANT = os.path.join(SRC, "assistant")
for p in (SRC, ASSISTANT):
    if p not in sys.path:
        sys.path.insert(0, p)
