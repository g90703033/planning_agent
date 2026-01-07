from typing import List, Dict, Any
from src.utils.llm import LLM
from src.core.memory import Memory

class Planner:
    def __init__(self, llm: LLM, memory: Memory):
        self.llm = llm
        self.memory = memory

    def create_plan(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Construct a prompt with context
        system_instruction = (
            "You are an expert coding agent. Return your plan as a JSON list of steps.\n"
            "Allowed step types:\n"
            "1. {\"type\": \"command\", \"command\": \"...\"} - Run a shell command.\n"
            "2. {\"type\": \"write_file\", \"filename\": \"...\", \"content\": \"...\"} - Write a file.\n"
            "3. {\"type\": \"read_file\", \"filename\": \"...\"} - Read a file.\n"
            "Note: You are working in a clean, isolated project directory. You do not need to create a folder."
        )
        
        prompt = f"Task: {task}\n\nEnvironment: {context}\n\n"
        if "files" in context:
            prompt += f"Files: {context['files']}\n\n"
            
        prompt += "Plan:"
        
        response = self.llm.generate(prompt, system_instruction)
        
        try:
            # Attempt to parse JSON response
            import json
            import re
            
            # Find JSON block using regex
            match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            
            # Fallback: try to find list brackets if no code blocks
            match = re.search(r"\[.*\]", response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
                
            # If strictly JSON
            return json.loads(response)
        except (json.JSONDecodeError, AttributeError):
            print(f"Failed to parse plan: {response}")
            # Fallback to a simple command if parsing fails
            return [{"type": "command", "command": f"echo 'Could not parse plan for: {task}'"}]

