from typing import Dict, Any
from src.core.memory import Memory

class Reflector:
    def __init__(self, memory: Memory):
        self.memory = memory

    def reflect(self, trace: Dict[str, Any]):
        # Analyze the trace and update procedural memory
        print("Reflecting on execution...")
        # Simple logic: if success, store as a successful pattern
        if trace.get("status") == "success":
            self.memory.update_procedural_memory({
                "trigger": trace.get("task"),
                "action": trace.get("plan")
            })
