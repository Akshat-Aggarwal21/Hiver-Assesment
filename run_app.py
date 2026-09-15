"""
1-Click Application Launcher for Hiver AI Email Copilot & Benchmark Suite.
Runs FastAPI + Uvicorn server hosting both REST APIs and the interactive Web Dashboard.
"""

import sys
from pathlib import Path
import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main():
    port = 8000
    host = "127.0.0.1"
    print("=" * 64)
    print("      HIVER AI — SHARED INBOX GENERATOR & EVALUATION SUITE      ")
    print("=" * 64)
    print(f"-> Web Application Dashboard: http://{host}:{port}")
    print(f"-> Interactive API Docs (Swagger): http://{host}:{port}/docs")
    print("-> Press Ctrl+C to stop the server.")
    print("=" * 64 + "\n")
    
    uvicorn.run("web.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
