import json
from pathlib import Path

MEMORY_FILE = Path("nocode/memory/sessions.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_memory():
    return json.loads(MEMORY_FILE.read_text()) if MEMORY_FILE.exists() else {}

def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

def append_message(session_id, role, content):
    memory = load_memory()
    memory.setdefault(session_id, []).append({"role": role, "content": content})
    save_memory(memory)

def get_history(session_id):
    memory = load_memory()
    return "\n".join(f"{m['role']}: {m['content']}" for m in memory.get(session_id, []))