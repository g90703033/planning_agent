from typing import List, Dict, Any
import json
import os

class Memory:
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = memory_file
        self.episodic_memory: List[Dict[str, Any]] = []
        self.procedural_memory: List[Dict[str, Any]] = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                data = json.load(f)
                self.episodic_memory = data.get("episodic", [])
                self.procedural_memory = data.get("procedural", [])

    def save_memory(self):
        data = {
            "episodic": self.episodic_memory,
            "procedural": self.procedural_memory
        }
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_trace(self, trace: Dict[str, Any]):
        self.episodic_memory.append(trace)
        self.save_memory()

    def get_procedural_rules(self) -> List[Dict[str, Any]]:
        return self.procedural_memory

    def update_procedural_memory(self, rule: Dict[str, Any]):
        self.procedural_memory.append(rule)
        self.save_memory()
