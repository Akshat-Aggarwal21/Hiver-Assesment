import sys
from pathlib import Path

# Ensure root directory is always on sys.path during pytest collection
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
